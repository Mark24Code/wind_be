from datetime import datetime
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
from itsdangerous import SignatureExpired, BadSignature

from app.exts import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String)
    role = db.Column(db.Integer, default=0)  # 角色： 0 普通用户，1 管理员
    status = db.Column(db.Integer, default=0)  # 状态：0 正常使用，1 停用， 2 删除
    created = db.Column(db.DateTime)  # 注册时间

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created = datetime.utcnow()

    @property
    def password(self):
        raise AttributeError('password is not readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=36000):
        jwt = JWT(current_app.config['SECRET_KEY'], expires_in=expiration)
        return jwt.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        jwt = JWT(current_app.config['SECRET_KEY'])
        try:
            data = jwt.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user
