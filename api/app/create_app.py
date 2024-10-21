
from database.models import User
from flask import Flask
from flask_login import LoginManager
from flask_caching import Cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

cache = Cache()

def create_app():
    app = Flask(__name__, 
                template_folder='../../client/templates',
                static_folder='../../client/static')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['CACHE_TYPE'] = 'SimpleCache' 
    cache.init_app(app)

    with app.app_context():
        from api import bp_views , bp_auth 
        app.register_blueprint(bp_views)
        app.register_blueprint(bp_auth)
   

    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user):
        return User.query.get(int(user))
    
    cache.init_app(app=app)

    return app