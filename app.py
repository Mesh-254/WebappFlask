import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from models.database import db
from models.Usermodel import User, Note
from flask_login import LoginManager, login_fresh

from blueprints.views import views
from blueprints.auth import auth


app = Flask('__name__')

DB_USERNAME = 'root'
DB_PASSWORD = ''
DB_NAME = 'webapp'
DB_SERVER = '127.0.0.1'
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.url_map.strict_slashes = False

db.app = app
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

app.template_folder = 'website/templates'


app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



if __name__ == '__main__':
    app.run(debug=True)
