from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.security import generate_password_hash
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
CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class BaseModel:

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Roles(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "register_time": self.register_time}

class Users(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), db.ForeignKey('roles.name'), nullable=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "role": self.role,
                "username": self.username,
                "register_time": self.register_time}

class FarmingChains(db.Model, BaseModel):
    __tablename__ = "farmingchains"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "register_time": self.register_time}

class Stages(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    idFarmingChain = db.Column(db.Integer, db.ForeignKey("farmingchains.id"), nullable=False)
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "register_time": self.register_time}

class MembersByStage(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    idStage = db.Column(db.Integer, db.ForeignKey("stages.id"), nullable=False)
    idMember = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "idStage": self.idStage,
                "idMember": self.idMember,
                "register_time": self.register_time}

class Members(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    identification_type = db.Column(db.String(8), nullable=False)
    identification = db.Column(db.String(15), nullable=False)
    member_type = db.Column(db.String(100))
    state = db.Column(db.Boolean())
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "address" : self.address,
                "phone" : self.phone,
                "identification_type" : self.identification_type,
                "identification" : self.identification,
                "participant_type" : self.participant_type,
                "state" : self.state,
                "register_time": self.register_time}

from .auth import auth_app as auth_blueprint
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
