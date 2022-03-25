import logging
from flask_migrate import Migrate
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import os 

DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_URI = os.environ["DB_URI"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=f'mariadb+pymysql://{DB_USER}:{DB_PASS}@{DB_URI}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = b'\xd3\xe4\x1c\xfeq\xf8\x9c\xd9{\x15\xb1\xfa\x13\xdf\xf9\xc3\xa9>\xe2\x91\x8c3\x94\xd1'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from .auth import auth_app as auth_blueprint
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
