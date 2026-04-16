import jwt
import os
from flask import request, jsonify
from models import User
from datetime import datetime, timezone, timedelta
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def generate_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(user_id)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')

        if not token:
            return jsonify({'message': 'Session expired or missing!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

            current_user = User.query.filter(User.user_id == data['sub']).first()
            print('user: {current_user}')

            if not current_user:
                raise ValueError("User not found")
        except:
            return jsonify({'message': 'Invalid session!'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated