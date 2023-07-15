from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from uuid import uuid4


class Driver(db.Model):
    __tablename__ = "driver"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer)
    name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin): 
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(345), unique=True) 
    password = db.Column(db.String(150))
    drivers = db.relationship('Driver')

