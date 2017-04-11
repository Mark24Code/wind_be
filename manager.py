import os

import click
from flask_migrate import Migrate

from app import create_app
from app.exts import db
from init import init_user

# Flask App Instance
app = create_app(os.environ['FLASK_CONFIG'])

# import all ORM tables

# migrate
migrate = Migrate(app, db)


# Flask CLI
@app.cli.command()
def init_dev():
    """Init data with database."""
    db.drop_all()
    db.create_all()
    click.echo('[ok] init databases')
    # init actions
    init_user()


@app.cli.command()
def drop():
    """Drop all databases."""
    db.drop_all()
    click.echo('[ok] drop databases')


@app.cli.command()
@click.option('--username', prompt='username', help='Account username.')
@click.option('--password', prompt='password', hide_input=True,
              confirmation_prompt=True, help='Account password.')
@click.option('--email', prompt='email', help='Account email.')
@click.option('--role', prompt='role', type=click.IntRange(0, 1), help='Super:1,User:0.')
def create_user(username, password, email, role):
    """Create account. --username,--password,--email,--role"""
    import hashlib
    from app.models.user import User
    md5 = hashlib.md5()
    md5.update(bytes(str(username) + str(password), encoding='utf8'))
    password_hash = md5.hexdigest()
    someone = User(
        username=username,
        password=password_hash,
        email=email,
        role=int(role),
        status=0
    )
    db.session.add(someone)
    db.session.commit()
    click.echo('created.')


@app.cli.command()
@click.option('--username', prompt='username', help='Account username.')
@click.option('--password', prompt='password', hide_input=True, help='Account password.')
@click.option('--newpassword', prompt='new password', confirmation_prompt=True, hide_input=True,
              help='Account new password.')
def change_password(username, password, newpassword):
    """change_password. --username,--password,--newpassword"""
    import hashlib
    from app.models.user import User
    md5 = hashlib.md5()
    md5.update(bytes(str(username) + str(password), encoding='utf8'))
    password_hash = md5.hexdigest()
    someone = User.query.filter_by(username=username).first()
    valid_flag = someone.verify_password(password_hash)

    if valid_flag:
        new_md5 = hashlib.md5()
        new_md5.update(bytes(str(username) + str(newpassword), encoding='utf8'))
        newpassword_hash = new_md5.hexdigest()
        someone.password = newpassword_hash
        db.session.add(someone)
        db.session.commit()
        click.echo('updated.')
    else:
        click.echo('username or password is wrong.Please try again.')


@app.cli.command()
def test():
    """ Start all unit test."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def migrate_files():
    """搬迁文件"""
    import shutil
    import os

    print('rm  files ...')
    try:
        shutil.rmtree('./app/static/css')
        shutil.rmtree('./app/static/js')
        shutil.rmtree('./app/static/fonts')
        shutil.rmtree('./app/static/img')
        os.remove('./app/templates/index.html')
    except FileNotFoundError:
        pass
    print('mv files ...')
    shutil.move('../FE/dist/static/js', './app/static/')
    shutil.move('../FE/dist/static/fonts', './app/static/')
    shutil.move('../FE/dist/static/css', './app/static/')
    shutil.move('../FE/dist/static/img', './app/static/')
    shutil.move('../FE/dist/index.html', './app/templates/')
    print('[OK] migrate finished.')
