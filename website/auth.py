from flask import Blueprint, request, jsonify, make_response, json
from .models import Dispatcher, Driver, Token
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.dialects.postgresql import insert
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

auth = Blueprint('auth', __name__)

def generate_token():
    import secrets
    return secrets.token_hex(16)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = Dispatcher.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return make_response(jsonify({"name": user.name, "email": user.email}), 200)
    driver = Driver.query.filter_by(email=email).first()
    if driver:
        if check_password_hash(driver.password, password):
            login_user(driver, remember=True)
            return make_response(jsonify({"name": driver.name, "email": driver.email}), 200)

    return make_response("Failed", 500)

@auth.route('/password', methods=['PUT'])
def index():
    data = request.get_json()
    email = data['email']
    smtp_server = "smtp.gmail.com"
    port = 587 

    sender_email = "nicoaradarius2007@gmail.com"
    sender_password = "eyysfzvwvheyjvcm"
    receiver_email = email
    subject = "Password change"

    token = generate_token()

    dispatcher = Dispatcher.query.filter_by(email=email).first()
    driver = Driver.query.filter_by(email=email).first()

    if dispatcher:
        token_db = Token(user_id = dispatcher.id,token = token)
    elif driver:
        token_db = Token(user_id = driver.id, token = token)
    else:
        return make_response("Email not found", 404)
    db.session.add(token_db)
    db.session.commit()

    body = f"http://127.0.0.1:5000/resetpassword/{token}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return make_response("Email sent successfully!", 200)
    except Exception as e:
        return(f"Failed to send email. Error: {e}", 400)
    
@auth.route('/resetpassword/<token>', methods=["POST"])
def resetpassword(token):
    # token = request.args.get('token')
    print(token)
    if request.method == 'POST':
        data = request.get_json()
        password = data['password']
        token_db = Token.query.filter_by(token=token).first()
        if token_db:
            driver = Driver.query.filter_by(id=token_db.user_id).first()
            dispatcher = Dispatcher.query.filter_by(id=token_db.user_id).first()
        if driver:
            driver.password = generate_password_hash(password, method='sha256')
            Token.query.filter_by(token=token).delete()
            db.session.commit()
            return make_response("Password reset successful.", 200)
        elif dispatcher:
            dispatcher.password = generate_password_hash(password, method='sha256')
            Token.query.filter_by(token=token).delete()
            db.session.commit()
            return make_response("Password reset successful.", 200)
        else:
            return make_response("Invalid or expired token.", 400)

@auth.route('/logout')
@auth.route('/user', methods=['GET'])
@login_required
def get_user_data():
    if isinstance(current_user, Driver):
        user_data = {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            # "phone_number": current_user.phone_number,
            "role": "driver",
        }
    else:
        user_data = {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "phone_number": current_user.phone_number,
            "role": "dispatcher",
        }
    return jsonify(user_data)
def logout():
    logout_user()
    return make_response("logout complete", 200)


@auth.route('/sign-up', methods=['POST'])
def signup():
    data = request.get_json()

    role = data['role']
    name = data['name']
    email = data['email']
    password = data['password']
    phone_number = data['phone_number']
    company = data['company']

    driver = Driver.query.filter_by(email=email).first()
    user = Dispatcher.query.filter_by(email=email).first()
    if user or driver:
        return make_response("Email already exists", 400)
    else:
        match role:
            case "driver":
                dispatcher = Dispatcher.query.filter_by(phone_number=phone_number).first()
                if dispatcher is None: 
                    return make_response("Dispatcher not found", 404)
                new_driver = Driver(name=name, email=email, password=generate_password_hash(password, method='sha256'),
                                    dispatcher_id=dispatcher.id, company = company)
                db.session.add(new_driver)
                db.session.commit()
            case "dispatcher":
                number_of_drivers = data['number_of_drivers']
                new_user = Dispatcher(name=name, email=email, password=generate_password_hash(password, method='sha256'),
                                phone_number=phone_number, company = company, number_of_drivers = number_of_drivers)
                db.session.add(new_user)
                db.session.commit()
        return make_response(jsonify({"Email": email, "Name": name}), 200)

@auth.route('/profile', methods=['PUT'])
@login_required
def edit_profile():
    data = request.get_json()
    email = data['email']
    name = data['name']
    phone_number = data['phone_number']

    if email:
        current_user.email = email
    if name:
        current_user.name = name
    if phone_number:
        current_user.phone_number = phone_number 
    db.session.commit()
    return make_response("Data changed", 200)


@auth.route('/driver', methods=['PUT'])
def remove_driver():
        if isinstance(current_user, Driver):
            return make_response("You are not a dispatcher", 401)
        data = request.get_json()
        id = data['id']
        driver = Driver.query.filter_by(id=id).first()
        driver.dispatcher_id = "Marinel"
        return make_response('Driver removed', 200)
