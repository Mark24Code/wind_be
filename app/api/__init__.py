from flask import jsonify, g
from app.models.user import User
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('JWT')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.auth_user = user
    return True


@token_auth.verify_token
def verify_token(token):
    if token:
        user = User.verify_token(token)
        if user:
            g.auth_user = user
            return True
        return False
    return False


@basic_auth.error_handler
def unauthorized(message=None):
    return jsonify({
        'status': 403,
        'message': message or 'forbidden',
        'data': {}
    }), 403


@token_auth.error_handler
def unauthorized(message=None):
    return jsonify({
        'status': 403,
        'message': message or 'forbidden',
        'data': {}
    }), 403
