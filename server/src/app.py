import os
import uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from models import db, User, Product, Category
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from session import generate_token, token_required
import os
from utils import generate_sku

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# API Utility
@app.route('/', methods=['GET'])
def server_status():
    return jsonify({
        "message": "Server is okay!",
    }), 200

@app.route('/static/uploads/<file_id>', methods=['GET'])
@token_required
def return_image(current_user, file_id):
    image_path = f'../static/uploads/{file_id}'
    return send_file(image_path, mimetype="image/png")

# API Account
@app.route("/auth/register", methods=['POST'])
def register_admin():
    if User.query.first():
        return jsonify({
            "success": False,
            "message": "1-Account Max: Admin alreadu exists. Only one user allowed."
        }), 403
    
    username = request.form.get('username')
    organization_name = request.form.get('organization_name')
    email = request.form.get('email')
    password = request.form.get('password')
    file = request.files.get('user_avatar')

    if not all([username, email, password]):
        return jsonify({
            "success": False,
            "message": "Invalid-Data: Missing required fields"
        }), 422

    avatar_path = None
    
    if file:
        filenamne = secure_filename(file.filename)
        avatar_path = os.path.join('static/uploads', f"admin_{uuid.uuid4().hex}_{filenamne}")
        file.save(avatar_path)
        image_path = image_path.replace("\\", "/")

    new_admin = User(
        user_id=str(uuid.uuid4()),
        username=username,
        organization_name=organization_name,
        email=email,
        password=generate_password_hash(password),
        user_avatar=avatar_path
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Created: Admin created successfully"
    }), 201

@app.route("/auth/login", methods=['POST'])
def login():
    data = request.form
    identifier = data.get('username')
    password = data.get('password')

    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    if user is None:
        return jsonify({
            "success": False,
            "message": "Not Found: Username and Email does not exist."
        }), 404

    if user and check_password_hash(user.password, password):
        user.last_login = datetime.now(timezone.utc)

        db.session.commit()

        token = generate_token(user.user_id)
        response = make_response(jsonify({
            "message": "Login successful",
            "user": {"username": user.username}
        }))

        response.set_cookie(
            'access_token',
            token,
            httponly=True,
            samesite="Lax",
            secure=False,
            max_age=60*60*24
        )

        return response
    
    return jsonify({
        "success": False,
        "message": "Missing: Invalid credentials"
    }), 401

@app.route('/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    response = make_response(jsonify({"message": f"Goodbye {current_user.username}"}))
    response.set_cookie('access_token', '', expires=0)
    return response

@app.route('/user', methods=['GET', 'PUT'])
@token_required
def get_profile(current_user):
    if request.method == 'GET':     
        user_brief = {
            "user_id": current_user.user_id,
            "username": current_user.username,
            "email": current_user.email,
            "userAvatar": current_user.user_avatar,
            "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
            "created_at": current_user.created_at.isoformat()
        }

        return jsonify({
            "success": True,
            "message": "Retrieved: User Profile",
            "data": user_brief
        }), 200
    else:
        username = request.form.get('username')
        organization_name = request.form.get('organization_name')
        email = request.form.get('email')
        file = request.files.get('user_avatar')

        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if organization_name:
            current_user.organization_name = organization_name

        if file and file.filename != '':
            if current_user.user_avatar and os.path.exists(current_user.user_avatar):
                try:
                    os.remove(current_user.user_avatar)
                except Exception as e:
                    print(f"Warning: Could not delete old avatar: {e}")

            filename = secure_filename(file.filename)
            unique_name = f"admin_{uuid.uuid4().hex}_{filename}"
            save_path = os.path.join('static/uploads', unique_name)
            file.save(save_path)

            current_user.user_avatar = save_path.replace("\\", "/")
        try:
            db.session.commit()
            return jsonify({
                "success": True,
                "message": "Updated: Profile information saved",
                "data": {
                    "username": current_user.username,
                    "user_avatar": current_user.user_avatar
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Database Error: {str(e)}"
            }), 500
            
# API CRUD for Category
@app.route("/category", methods=['POST'])
@token_required
def create_cateogry(current_user):
    category_name = request.form.get('category_name')
    
    if not category_name:
        return jsonify({
            "success": False,
            "message": "Invalid-Data: Missing required fields"
        }), 422
    
    if Category.query.filter(Category.category_name == category_name).first():
        return jsonify({
            "success": False,
            "message": "Duplicate: A same existing category name already exist."
        }), 409
    
    new_category = Category(
        category_id=str(uuid.uuid4()),
        category_name=str(category_name)
    )

    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Created: New category created successfully"
    }), 201

@app.route("/category", methods=['GET'])
@token_required
def read_categories(current_user):
    categories = Category.query.all()
    category_list = [
        {
            "category_id": category.category_id,
            "category_name": category.category_name
        }
        for category in categories
    ]

    return jsonify({
        "success": True,
        "message": "Retrieved: Categories read successfully",
        "data": category_list
    }), 200

@app.route("/category/<category_name>", methods=['GET'])
@token_required
def read_category(current_user, category_name):
    category = Category.query.filter(Category.category_name == category_name).first()

    if not category:
        return jsonify({
            "success": False,
            "message": f"Not Found: Category {category_name} does not exist",
        }), 404

    category_list = {
            "category_id": category.category_id,
            "category_name": category.category_name
    }

    return jsonify({
        "success": True,
        "message": "Retrieve: Category read successfully",
        "data": category_list
    }), 200


@app.route("/category/<category_cred>", methods=['PUT'])
@token_required
def update_category(current_user, category_cred):
    current_category = Category.query.filter((Category.category_id == category_cred) | (Category.category_name == category_cred)).first()
    new_name = request.form.get('new_name')

    if not current_category:
        return jsonify({
            "success": False,
            "message": f"Not Found: Category {category_cred} does not exist",
        }), 404
    
    current_category.category_name = new_name
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Updated: Successfully updated category name",
        "data": {
            "category_name": current_category.category_name
        }
    }), 200

@app.route("/category", methods=['DELETE'])
@token_required
def delete_category(current_user):
    category_cred = request.form.get('category_cred')
    current_category = Category.query.filter((Category.category_name == category_cred) | (Category.category_id == category_cred)).first()

    if not current_category:
        return jsonify({
            "success": False,
            "message": f"Not Found: Category {category_cred} does not exist",
        }), 404
    
    if current_category.products:
        return jsonify({
            "success": False,
            "message": "Conflict: Cannot delete category because it contains products. Move or delete products first."
        }), 409
    
    db.session.delete(current_category)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Deleted: Successfully deleted a category",
        "data": {
            "category_name": current_category.category_name
        }
    }), 200

# API CRUD for Products
@app.route("/products", methods=['POST'])
@token_required
def create_product(current_user):
    product_name = request.form.get('product_name')
    product_image = request.files.get('product_image')
    product_brand = request.form.get('product_brand')
    category_name = request.form.get('category_name')
    price = request.form.get('price', 0)
    quantity = request.form.get('quantity')

    if not all([product_name, product_image, product_brand, category_name, price, quantity]):
        return jsonify ({
            "success": False,
            "message": f"Missing: Missing required data.",
        }), 422

    category = Category.query.filter(Category.category_name == category_name).first()
    if not category:
        return jsonify({
            "success": False,
            "message": f"Not Found: Category {category_name} does not exist",
        }), 404
    
    sku = generate_sku(product_brand, category_name, product_name)
    image_path = None

    if product_image: 
        filename = secure_filename(product_image.filename)
        image_path = os.path.join('static/uploads', f"prod_{uuid.uuid4().hex}_{filename}")
        product_image.save(image_path)
        image_path = image_path.replace("\\", "/")


    new_product = Product(
            product_id=str(uuid.uuid4()),
            product_name=product_name,
            product_image=image_path,
            product_sku=sku,
            product_brand=product_brand,
            category_id=category.category_id,
            price=float(price),
            quantity=int(quantity)
        )
    
    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Created: Product added successfully",
        "data": {"sku": sku, "product_id": new_product.product_id}
    }), 201

@app.route("/products", methods=['GET'])
@token_required
def read_products(current_user):
    products = Product.query.all()
    product_list = [
        {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_image": product.product_image,
            "product_sku": product.product_sku,
            "product_brand": product.product_brand,
            "category_id": product.category_id,
            "price": product.price,
            "quantity": product.quantity,
            "updated_at": product.updated_at,
        }
        for product in products
    ]

    return jsonify({
        "success": True,
        "message": "Retrieve: Products read successfully",
        "data": product_list
    }), 200 

@app.route("/products/<product_id>", methods=['GET'])
@token_required
def product_detail(current_user, product_id):
    product = Product.query.filter(Product.product_id == product_id).first()
    if not product:
        return jsonify({
            "success": False,
            "message": f"Not Found: Category {product_id} does not exist",
        }), 404

    product_list = {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "product_image": product.product_image,
        "product_sku": product.product_sku,
        "product_brand": product.product_brand,
        "category_id": product.category_id,
        "price": product.price,
        "quantity": product.quantity,
        "updated_at": product.updated_at,
    }

    return jsonify({
        "success": True,
        "message": "Retrieve: Category read successfully",
        "data": product_list
    }), 200

@app.route("/products/<product_id>", methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    product_name = request.form.get('product_name')
    product_image = request.files.get('product_image')
    product_brand = request.form.get('product_brand')
    category_name = request.form.get('category_name')
    price = request.form.get('price', 0)
    quantity = request.form.get('quantity')

    current_product = Product.query.filter(Product.product_id == product_id).first()

    if product_name:
        current_product.product_name = product_name
    if product_brand:
        current_product.product_brand = product_brand
    if category_name:
        category = Category.query.filter(Category.category_name == category_name).first()
        current_product.category_id = category.category_id
    if price:
        current_product.price = price
    if quantity:
        current_product.quantity = quantity
    if product_image and product_image.filename != '':
        if current_product.product_image and os.path.exists(current_product.product_image):
            try:
                os.remove(current_product.product_image)
            except Exception as e:
                print(f"Warning: Could not delete old avatar: {e}")

        filename = secure_filename(product_image.filename)
        unique_name = f"admin_{uuid.uuid4().hex}_{filename}"
        save_path = os.path.join('static/uploads', unique_name)
        product_image.save(save_path)

        current_product.product_image = save_path.replace("\\", "/")

    db.session.commit()
    return jsonify({
        "success": True,
        "message": "Updated: Product information saved",
        "data": {
            "product_name": current_product.product_name,
            "product_image": current_product.product_image
        }
    }), 200

@app.route("/products", methods=['DELETE'])
@token_required
def delete_product(current_user):
    product_id = request.form.get('product_id')
    current_product = Product.query.filter(Product.product_id == product_id).first()

    if not current_product:
        return jsonify({
            "success": False,
            "message": f"Not Found: Product {product_id} does not exist",
        }), 404
    
    db.session.delete(current_product)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Deleted: Product information deleted",
        "data": {
            "product_name": current_product.product_name,
        }
    }), 200

@app.route("/search", methods=['GET'])
@token_required
def search_products(current_user):
    search = request.args.get('q')
    products = Product.query.filter(
        (Product.product_name.contains(search)) | 
        (Product.product_sku.contains(search))
    ).all()

    product_list = [
        {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_image": product.product_image,
            "product_sku": product.product_sku,
            "product_brand": product.product_brand,
            "category_id": product.category_id,
            "price": product.price,
            "quantity": product.quantity,
            "updated_at": product.updated_at,
        }
        for product in products
    ]

    return jsonify({
        "success": True,
        "message": "Retrieve: Product information retrieved",
        "data": product_list
    }), 200