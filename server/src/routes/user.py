import os
import uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify, make_response, send_file, Blueprint
from flask_cors import CORS
from models import db, User
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from session import generate_token, token_required
import os
from routes.products import product_bp
from routes.categories import category_bp
from routes.auth import auth_bp

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/static/uploads/<file_id>', methods=['GET'])
@token_required
def return_image(current_user, file_id):
    image_path = f'../static/uploads/{file_id}'
    return send_file(image_path, mimetype="image/png")

@user_bp.route('/user', methods=['GET', 'PUT'])
@token_required
def get_profile(current_user):
    if request.method == 'GET':     
        user_brief = {
            "user_id": current_user.user_id,
            "username": current_user.username,
            "organization_name": current_user.organization_name,
            "email": current_user.email,
            "user_avatar": current_user.user_avatar,
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