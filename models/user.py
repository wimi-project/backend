from app import db
from sqlalchemy.orm import relationship
from typing import List
from utils.encoders import custom_alchemy_encoder
import json


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    surname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String())
    salt = db.Column(db.String())
    position_lat = db.Column(db.Float)
    position_lon = db.Column(db.Float)
    feedbacks = relationship("Feedback")

    def __init__(
        self,
        name,
        surname,
        email,
        password,
        salt,
        position_lat,
        position_lon
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.salt = salt
        self.position_lat = position_lat
        self.position_lon = position_lon

    def __repr__(self):
        return '<User id {}>'.format(self.id)

    def to_json(self, include_feedbacks: bool) -> str:
        expand_additional: List[str] = ["feedbacks"] if include_feedbacks else []
        return (
            json.dumps(
                self,
                cls=custom_alchemy_encoder(False, expand_additional),
                check_circular=False
            )
        )
