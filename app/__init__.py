# coding: utf-8
import os
from flask import Flask
from flask_moment import Moment
from database import SQLALCHEMY

moment = Moment()
db = SQLALCHEMY()


def create_app(config_name):
    os.environ['APP_CONFIG_FILE'] = os.path.abspath(os.path.join(
            os.path.dirname(__file__), os.pardir, 'config',
            '{0}.py'.format(config_name)))

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')
    app.config.from_envvar('APP_CONFIG_FILE')

    moment.init_app(app)
    db.__init__(config_name)

    from .views.kana import kana
    app.register_blueprint(kana)

    from .views.errors import errors
    app.register_blueprint(errors)

    return app
