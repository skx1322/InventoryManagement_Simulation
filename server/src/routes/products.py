from flask import Blueprint, jsonify, request
import os
import uuid
from models import db, Product, Category
from werkzeug.utils import secure_filename
from session import token_required
import os
from utils import generate_sku

product_bp = Blueprint('product_bp', __name__)
# API CRUD for Products
@product_bp.route("/products", methods=['POST'])
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

@product_bp.route("/products", methods=['GET'])
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

@product_bp.route("/products/<product_id>", methods=['GET'])
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

@product_bp.route("/products/<product_id>", methods=['PUT'])
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

@product_bp.route("/products", methods=['DELETE'])
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

@product_bp.route("/search", methods=['GET'])
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