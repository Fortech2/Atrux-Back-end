from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from uuid import uuid4

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(345), unique=True) 
    password = db.Column(db.String(150))
    dispatcher_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(db.Model, UserMixin): 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(345), unique=True) 
    password = db.Column(db.String(150))
    phone_number = db.Column(db.Integer, unique=True)
    drivers = db.relationship('Driver')