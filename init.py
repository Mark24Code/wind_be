import hashlib
from app.exts import db
from app.models.user import User


def init_user():
    """
    初始化账号
    :return:
    """
    super_username = 'mark24'
    super_password = '123'
    super_md5 = hashlib.md5()
    super_md5.update(bytes(super_username + super_password, encoding='utf8'))
    super_password_hash = super_md5.hexdigest()
    super = User(
        username=super_username,
        password=super_password_hash,
        email="253899371@qq.com",
        role=1,
        status=0
    )
    common_username = 'atom'
    common_password = '123'
    common_md5 = hashlib.md5()
    common_md5.update(bytes(common_username + common_password, encoding='utf8'))
    common_password_hash = common_md5.hexdigest()
    common_user = User(
        username=common_username,
        password=common_password_hash,
        email="atom@qq.com",
        role=0,
        status=0
    )

    db.session.add(super)
    db.session.add(common_user)
    db.session.commit()
