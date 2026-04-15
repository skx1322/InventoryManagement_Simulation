import os
import uuid
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Product, Category
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from session import generate_token
import os

app = Flask(__name__)
CORS(app)

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

@app.route("/auth/register", methods=['POST'])
def register_admin():
    if User.query.first():
        return jsonify({
            "success": False,
            "message": "1-Account Max: Admin alreadu exists. Only one user allowed."
        }), 403
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    file = request.files.get('user_avatar')

    if not all([username, email, password]):
        return jsonify({
            "success": False,
            "message": "Invalid-Data: Missing required fields"
        }), 429

    avatar_path = None
    if file:
        filenamne = secure_filename(file.filename)
        avatar_path = os.path.join('static/uploads', f"admin_{uuid.uuid4().hex}_{filenamne}")
        file.save(avatar_path)
    
    new_admin = User(
        user_id=str(uuid.uuid4()),
        username=username,
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
    data = request.get_json()
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

        return jsonify({
            "success": True,
            "message": "Login: Admin login successfully",
            "token": token
        }), 200
    
    return jsonify({
        "success": False,
        "message": "Missing: Invalid credentials"
    }), 401