from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    user_avatar= db.Column(db.String(128))
    password = db.Column(db.String(64), primary_key=True)
    last_login = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Category(db.Model):
    category_id = db.Column(db.String(64), primary_key=True)
    category_name = db.Column(db.String(128), nullable=False, unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    product_id = db.Column(db.String(64), primary_key=True)
    product_name = db.Column(db.String(256), nullable=False, unique=True)
    product_image= db.Column(db.String(128))
    product_sku = db.Column(db.String(128), nullable=False, unique=True)
    category_id = db.Column(db.String(64), db.ForeignKey('category.category_id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))