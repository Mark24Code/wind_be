from flask import Flask
from flask_cors import CORS
from .exts import db
from .config import config

from app.index import bp as index_bp
from app.api.v_1_0 import bp as v_1_0_bp


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)

    app.register_blueprint(index_bp)
    app.register_blueprint(v_1_0_bp)

    CORS(app, resources=r'/api/*')

    return app
