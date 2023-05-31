from flask import Flask ,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from os import path
import os , threading
from flask_login import LoginManager
from flask_restful import Api,Resource
from flask_migrate import Migrate
from replit import db
from flask_mail import Mail, Message
from flask import Blueprint, render_template
from flask_ckeditor import CKEditor
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
dbsql = SQLAlchemy()
DB_NAME = "database.db"
basedir = os.path.abspath(os.path.dirname(__file__))
import socket , pickle , time

def page_not_found(e):
   return render_template('404.html'), 404
def create_app():
    app = Flask(__name__)
    #Add Editor
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","JPEG","JPG","GIF"]
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'trcyclop@gmail.com'
    app.config['MAIL_PASSWORD'] = 'maltepe123'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    api = Api(app)    
    dbsql.init_app(app)
    migrate = Migrate(app,dbsql)
    from .views import views
    from .auth import auth
    

    from .models import User
    with app.app_context():
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(500, page_not_found)
        dbsql.create_all()
        print('Database Yaratıldı')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    ckeditor = CKEditor(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app 
