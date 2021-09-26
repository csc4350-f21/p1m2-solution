from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    username = db.Column(db.String(80), primary_key=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Artist(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), foreign_key=True, nullable=False)

    def __repr__(self):
        return f"<Artist {self.artist_id}>"