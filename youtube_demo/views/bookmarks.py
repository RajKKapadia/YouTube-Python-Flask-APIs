import uuid

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from youtube_demo.utils.bookmarks_responses import *
from youtube_demo.constants.http_status_codes import *
from youtube_demo.database.bookmarks_database import *


bookmarks = Blueprint(
    'bookmarks',
    __name__,
    url_prefix='/api/v1/bookmarks'
)


@bookmarks.post('/create')
@jwt_required()
def create():
    if request.is_json:
        data = request.get_json()
        url = data['url']
        remarks = data['remarks']
        bookmark = get_bookmark_by_url(url)
        if bookmark:
            return format_bookmarks_create_update_delete('Url already exists.'), HTTP_409_CONFLICT
        else:
            user = get_jwt_identity()
            bookmark = {
                'url': url,
                'email': user['email'],
                'visits': 0,
                'remarks': remarks,
                'shorten_url': str(uuid.uuid1())
            }
            _ = create_bookmark(bookmark)
            return format_bookmarks_create_update_delete('Bookmark created.'), HTTP_201_CREATED
    else:
        return format_bookmarks_create_update_delete('Bad request.'), HTTP_400_BAD_REQUEST


@bookmarks.post('/get/all')
@jwt_required()
def get_all():
    user = get_jwt_identity()
    all_bookmarks = get_bookmarks(user['email'])
    return format_bookmarks_get('Success', all_bookmarks)


@bookmarks.post('/get/one/<string:id>')
@jwt_required()
def get_one(id):
    try:
        all_bookmarks = get_bookmark_by_id(id)
        if all_bookmarks:
            return format_bookmarks_get('Success.', [all_bookmarks])
        else:
            return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT
    except:
        return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT


@bookmarks.post('/update/<string:id>')
@jwt_required()
def update_one(id):
    if request.is_json:
        try:
            all_bookmarks = get_bookmark_by_id(id)
            if all_bookmarks:
                data = request.get_json()
                update = data['update']
                _ = update_bookmark_by_id(id, update)
                return format_bookmarks_create_update_delete('Success.'), HTTP_200_OK
            else:
                return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT
        except:
            return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT
    else:
        return format_bookmarks_create_update_delete('Bad request.'), HTTP_400_BAD_REQUEST


@bookmarks.post('/delete/<string:id>')
@jwt_required()
def delete_one(id):
    try:
        all_bookmarks = get_bookmark_by_id(id)
        if all_bookmarks:
            _ = update_bookmark_by_id(id, {'is_deleted': True})
            return format_bookmarks_create_update_delete('Success.'), HTTP_200_OK
        else:
            return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT
    except:
        return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT


@bookmarks.post('/get/shorten/<string:shorten_url>')
@jwt_required()
def get_shorte(shorten_url):
    try:
        all_bookmarks = get_bookmark_by_shorten_url(shorten_url)
        if all_bookmarks:
            _ = update_bookmark_by_id(all_bookmarks['_id'], {'visits': all_bookmarks['visits'] + 1})
            return format_bookmarks_get('Success.', [all_bookmarks])
        else:
            return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT
    except:
        return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT
    