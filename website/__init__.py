from flask import Flask
from sqlalchemy import create_engine
import pandas as pd

SERVER = 'DESKTOP-N60GPF0\MSSQLSERVER'
DATABASE = 'inventory'
DRIVER = 'ODBC Driver 17 for SQL Server'
USERNAME = 'mualaa'
PASSWORD = 'P@ssw0rd'
DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

engine = create_engine(DATABASE_CONNECTION)
conn = engine.connect()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SrTtmiCk4rWchPCaxNY7Xtb5XwELFrvV'
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app
