from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager 

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
   
  
    # Define the static folder and URL path
    app.static_folder = 'static'  # Folder where your static files are located
    app.static_url_path = '/static'  # URL prefix for static files

    # Import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix='/auth')
    
    from .models import Mentor , Image , Favorite
    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Mentor.query.get(int(id))
    
    return app


 #database creation
def create_database(app):
   with app.app_context():
     db.create_all()
