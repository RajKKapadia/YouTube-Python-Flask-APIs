from flask import Blueprint, jsonify

from config import config

home = Blueprint(
    'home',
    __name__,
    url_prefix=config.URL_PREFIX
)


@home.route('/', methods=['GET', 'POST'])
def index():
    return jsonify(
        {
            'status': True,
            'message': 'Working okay...',
            'version': '1.0.0'
        }
    )
