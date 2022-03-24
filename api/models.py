from time import timezone
from . import db
from flask_login import UserMixin

class BaseModel:

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Users(db.Model, UserMixin, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)
    