from flask import Flask
from .config import DevConfig, Test
from app.extensions import db, migrate
from .models import *


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    return app
