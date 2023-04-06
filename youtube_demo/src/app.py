import os

from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from youtube_demo.views.home import home
from youtube_demo.views.auth import auth
from youtube_demo.views.bookmarks import bookmarks

load_dotenv('.env')

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
)
jwt = JWTManager(app)

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(bookmarks)
