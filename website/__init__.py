from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def make_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Cristian1981.@mypostgres.postgres.database.azure.com/test'

    db.init_app(app)

    from .views import views
    from .auth import auth
    from .add_route import chat

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(chat, url_prefix="/")

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

    return app