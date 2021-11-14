
from flask import Flask
from views.surv import surv

def create_app():
    app = Flask(__name__)
    app.register_blueprint(surv, url_prefix='/surv')

    return app