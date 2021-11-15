import os

from flask import Flask

from views.surv import surv

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(surv, url_prefix='/surv')

    return app