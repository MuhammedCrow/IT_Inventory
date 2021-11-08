from flask import Flask
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SrTtmiCk4rWchPCaxNY7Xtb5XwELFrvV'
    app.permanent_session_lifetime = timedelta(days=5)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app
