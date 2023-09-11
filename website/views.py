import io

import PIL.Image
from flask import Blueprint, make_response
from flask_login import login_required, current_user

from .models import Driver

views = Blueprint('views', __name__)

@views.route('/', methods=['POST'])
def home():
    # print(image.user_id)
    print(len(current_user.images[0].img))
    imag = PIL.Image.open(io.BytesIO(current_user.images[0].img))
    imag.save('nume_poza4124.png')
    return make_response("Success", 200)

@views.route('/drivers', methods=['GET'])
@login_required
def get_drivers():
    if isinstance(current_user, Driver):
        return make_response("You are not a dispatcher", 400)
    return current_user.drivers[0].name
