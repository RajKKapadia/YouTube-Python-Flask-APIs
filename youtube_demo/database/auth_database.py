import os
from datetime import datetime
from typing import Any

from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv('.env')

client = MongoClient(os.getenv('MONGODB_URL'))

DB_NAME = client['YoutubePythonAPI']

users = DB_NAME['users']


def create_user(user: dict) -> bool:
    user['created_at'] = datetime.now()
    user['password'] = generate_password_hash(user['password'])
    result = users.insert_one(user)
    return result.acknowledged

def get_user(email: str) -> Any:
    user = users.find_one({'email': email})
    if user:
        return user
    else:
        return None
    
def verify_user(email: str, password: str) -> bool:
    user = get_user(email)
    if user:
        is_valid = check_password_hash(user['password'], password)
        if is_valid:
            return True
        else:
            return False
    else:
        return False
