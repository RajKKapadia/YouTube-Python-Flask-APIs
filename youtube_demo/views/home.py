from flask import Blueprint, jsonify

home = Blueprint(
    'home',
    __name__,
    url_prefix='/api/v1'
)


@home.route('/', methods=['GET', 'POST'])
def index():
    return jsonify(
        {
            'status': True,
            'msg': 'Working okay...',
            'version': '1.0.0'
        }
    )
