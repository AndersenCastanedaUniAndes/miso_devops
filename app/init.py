from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db:SQLAlchemy = SQLAlchemy()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blacklist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
