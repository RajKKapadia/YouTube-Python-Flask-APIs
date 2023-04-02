from flask import Flask

from youtube_demo.views.home import home
from youtube_demo.views.auth import auth

app = Flask(__name__)

app.register_blueprint(home)
app.register_blueprint(auth)
