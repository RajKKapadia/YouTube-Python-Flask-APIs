from flask import Blueprint, jsonify

auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/api/v1/auth'
)


@auth.get('/users/<id>')
def get_all_users(id):
    print(id)
    return []

@auth.post('/users/register')
def register():
    return 'User created...'