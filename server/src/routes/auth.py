from flask import Blueprint, jsonify, request, make_response
import os
import uuid
from models import User, db
from werkzeug.utils import secure_filename
from session import token_required
import os
from werkzeug.security import generate_password_hash, check_password_hash
from session import generate_token, token_required
from datetime import datetime, timezone

auth_bp = Blueprint('auth_bp', __name__)

# API Account
@auth_bp.route("/auth/register", methods=['POST'])
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

@auth_bp.route("/auth/login", methods=['POST'])
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
            "success": True,
            "message": "Login successful",
            "data": {"username": user.username, "token": token}
        }))

        response.set_cookie(
            'access_token',
            token,
            path="/",
            httponly=True,
            samesite="lax",
            secure=False,
            max_age=60*60*24
        )

        return response
    
    return jsonify({
        "success": False,
        "message": "Missing: Invalid credentials"
    }), 401

@auth_bp.route('/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    response = make_response(jsonify({"message": f"Goodbye {current_user.username}"}))
    response.set_cookie('access_token', '', expires=0)
    return response
