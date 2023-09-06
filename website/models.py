from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from uuid import uuid4

def get_uuid():
    return uuid4().hex


class raspberry(db.Model):
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid)
    driver_email = db.Column(db.String(345), unique=True)

class Root_Notification(db.Model):
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(100), db.ForeignKey('drivers.id'))
    content = db.Column(db.String(500))
    expiration = db.Column(db.String(100))
class Alarm_Notification(db.Model):
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(100), db.ForeignKey('drivers.id'))
    img = db.Column(db.LargeBinary)
    date = db.Column(db.String(100))

class Token(db.Model, UserMixin):
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(100))
    token = db.Column(db.String(100))
    expiration = db.Column(db.String(100))
class Driver(db.Model, UserMixin):
    __tablename__ = 'drivers'
    id = db.Column(db.String(100), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(150))
    email = db.Column(db.String(345), unique=True)
    phone_number = db.Column(db.String(11), unique=True)
    password = db.Column(db.String(150))
    company = db.Column(db.String(150))
    route = db.Column(db.String(500))
    dispatcher_id = db.Column(db.String(100), db.ForeignKey('users.id'))
    active = db.Column(db.String(1), default='0')
    rbid = db.Column(db.String(100))
    alarm_notifications = db.relationship('Alarm_Notification')
    root_notification = db.relationship('Root_Notification')

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