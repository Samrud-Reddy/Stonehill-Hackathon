import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

def create_jwt_token(phone_number: str, upi_id: str) -> str:
    secret_key = os.getenv('SECRET_KEY')
    algorithm = 'HS256'
    payload = create_payload(phone_number=phone_number, upi_id=upi_id)
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def salt_hash_pin(upi_pin: str) -> str:
    salt = os.urandom(32)
    hashed_pin = hashlib.pbkdf2_hmac('sha256', upi_pin.encode('utf-8'), salt, 100000)
    return hashed_pin, salt

def create_payload(phone_number: str, upi_id: str) -> dict:
    
    payload = {
        'phone_number': f"{phone_number}",
        'upi_id': f"{upi_id}",
        'exp': datetime.now(timezone.utc) + timedelta(weeks=26)}
    
    return payload

def validate_jwt_token(jwt_token: str):
    secret_key = os.getenv('SECRET_KEY')
    algorithm = 'HS256'
    
    try:
        decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=[algorithm])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False