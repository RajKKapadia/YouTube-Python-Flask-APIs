import os
from datetime import datetime
from typing import Any, List
from bson import ObjectId

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('.env')

client = MongoClient(os.getenv('MONGODB_URL'))

DB_NAME = client['YoutubePythonAPI']

bookmarks = DB_NAME['bookmars']


def create_bookmark(bookmark: dict) -> bool:
    bookmark['created_at'] = datetime.now()
    bookmark['is_deleted'] = False
    result = bookmarks.insert_one(bookmark)
    return result.acknowledged


def get_bookmark_by_url(url: str) -> Any:
    bookmark = bookmarks.find_one({'url': url, 'is_deleted': False})
    if bookmark:
        bookmark['_id'] = str(bookmark['_id'])
        return bookmark
    else:
        return None


def get_bookmarks(email: str) -> List[dict]:
    cursor = bookmarks.find({'email': email, 'is_deleted': False})
    all_bookmarks = []
    for item in cursor:
        item['_id'] = str(item['_id'])
        all_bookmarks.append(item)
    if len(all_bookmarks) > 0:
        return all_bookmarks
    else:
        return [{}]


def get_bookmark_by_id(id: str) -> Any:
    bookmark = bookmarks.find_one({'_id': ObjectId(id), 'is_deleted': False})
    if bookmark:
        bookmark['_id'] = str(bookmark['_id'])
        return bookmark
    else:
        return None


def update_bookmark_by_id(id: str, update: dict) -> Any:
    bookmark = bookmarks.find_one_and_update(
        {
            '_id': ObjectId(id),
            'is_deleted': False
        },
        {
            '$set': update
        }
    )
    if bookmark:
        bookmark['_id'] = str(bookmark['_id'])
        return bookmark
    else:
        return None
    
def get_bookmark_by_shorten_url(shorten_url: str) -> Any:
    bookmark = bookmarks.find_one({'shorten_url': shorten_url, 'is_deleted': False})
    if bookmark:
        bookmark['_id'] = str(bookmark['_id'])
        return bookmark
    else:
        return None
