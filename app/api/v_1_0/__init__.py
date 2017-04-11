from flask import Blueprint
from flask_restful import Api, Resource

from app.libs.utils import import_all_modules

bp = Blueprint('api.v_1_0', __name__, url_prefix='/api/v1.0')

restful_api = Api(bp)

import_all_modules(__name__,include_packages=True, recursive=True)
