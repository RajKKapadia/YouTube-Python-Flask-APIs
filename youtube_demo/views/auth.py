from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from youtube_demo.constants.http_status_codes import *
from youtube_demo.database.database import create_user, get_user, verify_user
from youtube_demo.utils.formated_responses import format_auth_register, format_auth_verify, format_auth_me, format_auth_refresh_token

auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/api/v1/auth'
)


@auth.post('/users/register')
def register():
    if request.is_json:
        body = request.get_json()
        user = get_user(body['email'])
        if user:
            return format_auth_register('User already exists.'), HTTP_409_CONFLICT
        else:
            _ = create_user(body)
            format_auth_register('User created.'), HTTP_201_CREATED
    else:
        return format_auth_register('Request has no body.'), HTTP_400_BAD_REQUEST


@auth.post('/users/verify')
def verify():
    if request.is_json:
        body = request.get_json()
        flag = verify_user(body['email'], body['password'])
        if flag:
            access_token = create_access_token(
                {'email': body['email']})
            refresh_token = create_refresh_token(
                {'email': body['email']})
            return format_auth_verify('Success.', access_token, refresh_token), HTTP_200_OK
        else:
            return format_auth_verify('Wrong email or password.', '', ''), HTTP_401_UNAUTHORIZED

    else:
        return format_auth_verify('Request has no body.', access_token, refresh_token), HTTP_400_BAD_REQUEST


@auth.get('/users/get')
@jwt_required()
def get_user():
    user = get_jwt_identity()
    return format_auth_me('Success.', user), HTTP_200_OK

@auth.get('/users/refresh/token')
@jwt_required()
def refresh_token():
    user = get_jwt_identity()
    access_token = create_access_token(user)
    return format_auth_refresh_token('Success.', access_token), HTTP_200_OK
