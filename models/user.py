from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import relationship

from app import db
from models import Feedback


@dataclass
class User(db.Model):

    __tablename__ = 'user'

    user_id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(), nullable=False)
    surname: str = db.Column(db.String(), nullable=False)
    email: str = db.Column(db.String(), nullable=False, unique=True)
    password: str = db.Column(db.String())
    salt: str = db.Column(db.String())
    position_lat: float = db.Column(db.Float)
    position_lon: float = db.Column(db.Float)

    visited_commercial_activities = relationship(
        "CommercialActivity",
        secondary="visit",
    )
    feedbacks = relationship("Feedback")

    def __init__(
        self,
        name,
        surname,
        email,
        user_id=None,
        password=None,
        salt=None,
        position_lat=None,
        position_lon=None
    ):
        self.name = name
        self.surname = surname
        self.email = email
        self.user_id = user_id
        self.password = password
        self.salt = salt
        self.position_lat = position_lat
        self.position_lon = position_lon

    def __repr__(self):
        return '<User id {}>'.format(self.id)
