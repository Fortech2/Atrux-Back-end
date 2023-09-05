from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import time
from flask_login import login_user, login_required, logout_user, current_user
from app import app ,handle_to_server, handle_notification, handle_images

db = SQLAlchemy()
DB_NAME = "database.db"

import pika, os
import PIL.Image
import io
import base64
import random
import string
import json
from threading import Thread
from .models import Images
url = os.environ.get('CLOUDAMQP_URL', 'amqps://zqbavobe:8LsWyHTXCdM2lFB0AbUS-540BCdksEBM@cow.rmq2.cloudamqp.com/zqbavobe')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue

def callback(ch, method, properties, body):
    json_data = json.loads(body)
    image_str : str = json_data['image']
    email = json_data['email']
    uuid = json_data['uuid']
    image_str = image_str[2:]
    image_str = image_str[:-1]
    raw_bytes = base64.b64decode(image_str)

    # print(len(image_str))
    # print(len(image_str))
    b = base64.b64decode(raw_bytes)
    #print(raw_bytes)
    imag = PIL.Image.open(io.BytesIO(raw_bytes))
    imag.save('nume_poza.png')

    print(len(raw_bytes))

    with app.app_context():
        img = Images(user_id = uuid, img = raw_bytes)
        db.session.add(img)
        db.session.commit()

    print(email)
    handle_to_server(uuid)
    handle_images(email)
    
    # with open("poze.jpg", "wb") as binary_file:
    #     binary_file.write(raw_bytes)
    #     binary_file.close()
def read():
    channel.basic_consume('hello',
                          callback,
                          auto_ack=True)
    print(' [*] Waiting for messages:')
    channel.start_consuming()
    connection.close()

token_cleanup_thread = Thread(target=read)
token_cleanup_thread.start()


app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Cristian1981.@mypostgres.postgres.database.azure.com/test'
db.init_app(app)

from .views import views
from .auth import auth
from .add_route import chat
from .change_active_status import active_status

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(chat, url_prefix="/")
app.register_blueprint(active_status, url_prefix="/")

from .models import Dispatcher, Driver

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = Dispatcher.query.get(user_id)
    if not user:
        user = Driver.query.get(user_id)
    return user

if __name__ == "__main__":
    pass