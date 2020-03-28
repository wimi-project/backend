from app import db
from sqlalchemy.orm import relationship
from typing import List
from utils.encoders import custom_alchemy_encoder
import json


class CommercialActivity(db.Model):
    __tablename__ = 'commercial_activity'

    commercial_activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String())
    position_lat = db.Column(db.Float)
    position_lon = db.Column(db.Float)
    queue_time = db.Column(db.Integer)
    products = db.relationship("Offer")

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
        return '<CommercialActivity id {}>'.format(self.id)

    def to_json(self, include_feedbacks: bool) -> str:
        return (
            json.dumps(
                self,
                cls=[],
                check_circular=False
            )
        )
