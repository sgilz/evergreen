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
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
