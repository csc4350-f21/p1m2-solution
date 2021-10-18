import flask
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from flask_login import UserMixin

db = SQLAlchemy(app)
