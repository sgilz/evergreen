from time import timezone
from . import db

class BaseModel:

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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

class Roles(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    register_time = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "register_time": self.register_time}

class FarmingChains(db.Model, BaseModel):
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