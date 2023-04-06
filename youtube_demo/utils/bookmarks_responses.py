from typing import List

from flask import jsonify


def format_bookmarks_create_update_delete(msg: str) -> jsonify:
    return jsonify(
        {
            'msg': msg
        }
    )

def format_bookmarks_get(msg: str, bookmarks: List[dict]) -> jsonify:
    return jsonify(
        {
            'msg': msg,
            'bookmarks': bookmarks
        }
    )
