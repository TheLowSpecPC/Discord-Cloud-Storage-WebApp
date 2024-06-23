from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY'

    from .views import Views
    from .auth import Auth

    app.register_blueprint(Views, url_prefix = '/')
    app.register_blueprint(Auth, url_prefix='/')

    return app