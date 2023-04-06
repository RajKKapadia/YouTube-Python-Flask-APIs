import os
from datetime import datetime

from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv('.env')

client = MongoClient(os.getenv('MONGODB_URL'))

DB_NAME = client['YoutubePythonAPI']

users = DB_NAME['users']
bookmarks = DB_NAME['bookmars']


def create_user(user: dict) -> bool:
    user['created_at'] = datetime.now()
    user['password'] = generate_password_hash(user['password'])
    result = users.insert_one(user)
    return result.acknowledged

def get_user(email: str) -> bool:
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

# print(create_user(
#     {
#         'user_name': 'Raj',
#         'email': 'raj@gmail.com',
#         'password': 'ancd1234',
#         'created_at': datetime.now()
#     }
# ))

# print(get_user('raj@gmjail.com'))
# print(generate_password_hash('abcd1234').split(':')[-1])
# print(check_password_hash('pbkdf2:sha256:260000$1NZ2MyE1xiGaZ7rn$e8f97f78579f969ff8e964a76e9cc38967952681ed0df13al8034dc1d8b2397c', 'abcd1234'))
