import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
import secrets

from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    songs = db.relationship('Song', back_populates="user")

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(str(self.password), str(password))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_all():
        return User.query.all()


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(150), nullable=True, default='')
    guitar = db.Column(db.String(150), nullable=True, default='')
    amp = db.Column(db.String(150), nullable=True, default='')
    pedals = db.Column(db.String(150), nullable=True, default='')
    style = db.Column(db.String(150), nullable=True, default='')
    groove = db.Column(db.String(150), nullable=True, default='')
    user = db.relationship('User', back_populates="songs")

    def __repr__(self):
        return f'Song {self.name} has been added to the database'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Song.query.get(id)

    @staticmethod
    def get_by_user_id(userId):
        return Song.query.filter(Song.user_id == userId)

    @staticmethod
    def get_all():
        return Song.query.all()