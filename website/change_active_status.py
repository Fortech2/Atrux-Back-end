from flask_login import login_required, current_user
from flask import Blueprint, request, make_response
from .models import Driver
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
    return make_response("Route changed", 200)