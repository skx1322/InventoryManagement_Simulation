import jwt
import os
from datetime import datetime, timezone, timedelta
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def generate_token(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")