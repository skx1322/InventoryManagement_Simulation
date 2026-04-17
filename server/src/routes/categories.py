from flask import Blueprint, jsonify, request
import uuid
from models import db, Category
from session import token_required

category_bp = Blueprint('category_bp', __name__)

# API CRUD for Category
@category_bp.route("/category", methods=['POST'])
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

@category_bp.route("/category", methods=['GET'])
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

@category_bp.route("/category/<category_name>", methods=['GET'])
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


@category_bp.route("/category/<category_cred>", methods=['PUT'])
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

@category_bp.route("/category", methods=['DELETE'])
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
