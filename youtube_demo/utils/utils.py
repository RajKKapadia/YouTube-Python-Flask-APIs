from flask import jsonify


def format_auth_register(msg: str) -> jsonify:
    return jsonify(
        {
            'msg': msg
        }
    )


def format_auth_verify(msg: str, access_token: str, refrsh_token: str) -> jsonify:
    return jsonify(
        {
            'msg': msg,
            'access_token': access_token,
            'refresh_toekn': refrsh_token
        }
    )
