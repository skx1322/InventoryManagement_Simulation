from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes.products import product_bp
from routes.categories import category_bp
from routes.auth import auth_bp
from routes.user import user_bp

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

app.register_blueprint(user_bp)

app.register_blueprint(auth_bp)

app.register_blueprint(category_bp)

app.register_blueprint(product_bp)
