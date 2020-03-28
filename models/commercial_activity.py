from app import db
from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import relationship


@dataclass
class CommercialActivity(db.Model):
    __tablename__ = 'commercial_activity'

    commercial_activity_id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(), nullable=False)
    address: str = db.Column(db.String())
    position_lat: float = db.Column(db.Float)
    position_lon: float = db.Column(db.Float)
    queue_time: int = db.Column(db.Integer)

    products = db.relationship("Product", secondary="offer")

    users_that_visited = relationship(
        "User",
        secondary="visit",
    )

    def __init__(
        self,
        name,
        position_lat,
        position_lon,
        address=None,
        queue_time=None,
        commercial_activity_id=None,
    ):
        self.name = name
        self.position_lat = position_lat
        self.position_lon = position_lon
        self.address = address
        self.queue_time = queue_time
        self.commercial_activity_id = commercial_activity_id

    def __repr__(self):
        return '<CommercialActivity id {}>'.format(self.id)
