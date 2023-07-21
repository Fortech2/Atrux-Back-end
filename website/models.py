from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from uuid import uuid4

def get_uuid():
    return uuid4().hex

class Driver(db.Model, UserMixin):
    __tablename__ = 'drivers'
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(150))
    email = db.Column(db.String(345), unique=True) 
    password = db.Column(db.String(150))
    company = db.Column(db.String(150))
    dispatcher_id = db.Column(db.String(100), db.ForeignKey('users.id'))

class Dispatcher(db.Model, UserMixin): 
    __tablename__ = "users"
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(150))
    email = db.Column(db.String(345), unique=True) 
    password = db.Column(db.String(150))
    phone_number = db.Column(db.String(11), unique=True)
    company = db.Column(db.String(150))
    number_of_drivers = db.Column(db.Integer, default=0)
    drivers = db.relationship('Driver')