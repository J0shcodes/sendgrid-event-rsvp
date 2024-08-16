from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import os
from config import config

db = SQLAlchemy()

def create_app():
        
    app = Flask(__name__)
    
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[env])
    SENDGRID_API_KEY = app.config['SENDGRID_API_KEY']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./events.db'

    db.init_app(app)

    from routes import create_routes

    create_routes(app, db, SENDGRID_API_KEY)

    migrate = Migrate(app, db)

    return app
