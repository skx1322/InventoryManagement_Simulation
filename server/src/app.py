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

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

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
                    "userAvatar": current_user.user_avatar
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"Database Error: {str(e)}"
            }), 500
            
# CRUD for Category
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
        "message": "Created: New category created successfully",
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
        "message": "Created: New category created successfully",
        "data": category_list
    }), 200


@app.route("/category/<category_cred>", methods=['PUT'])
@token_required
def updaet_category(current_user, category_cred):
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
    current_category = Category.query.filter((Category.category_id == category_cred) | (Category.category_name == category_cred)).first()

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

# CRUD for Products
@app.route("/products", methods=['POST'])
@token_required
def create_product(current_user):
    product_name = request.form.get('product_name')
    product_image = request.files.get('product_image')

    return

@app.route("/products", methods=['GET'])
@token_required
def read_product(current_user):
    return

@app.route("/products", methods=['PUT'])
@token_required
def updaet_product(current_user):
    return

@app.route("/products", methods=['DELETE'])
@token_required
def delete_product(current_user):
    return