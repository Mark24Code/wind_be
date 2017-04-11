from flask import g
from flask_restful import Resource
from .. import basic_auth
from . import restful_api


class Token(Resource):
    decorators = [basic_auth.login_required]

    def get(self):
        token = g.auth_user.generate_auth_token()
        return {
            'token': token.decode('ascii')
        }


restful_api.add_resource(Token, '/token')
