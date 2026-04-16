import os
from flask import Flask
from .database import db


def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///beacon.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["TESTING"] = False

    if config:
        app.config.update(config)

    db.init_app(app)

    from .routes import register_blueprints
    register_blueprints(app)

    return app
