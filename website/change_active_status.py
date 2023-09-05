from flask_login import login_required, current_user
from flask import Blueprint, request, make_response
from .models import raspberry
from . import db
from app import  handle_notification

active_status = Blueprint('active_status', __name__)

@active_status.route("/active", methods=["POST"])
@login_required
def change_active():
    data = request.get_json()
    active_status = data["active_status"]
    current_user.active = active_status
    db.session.commit()
    return make_response("Status changed", 200)

@active_status.route("CreateRB", methods=["POST"])
def CreateRB():
    rasp = raspberry()
    db.session.add(rasp)
    db.session.commit()
    return make_response("Added raspberry in db", 200)
    