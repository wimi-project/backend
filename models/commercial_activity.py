import logging
from dataclasses import dataclass

from sqlalchemy.orm import relationship

from app import db

logger = logging.getLogger("main")


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

    def serialize(self, include_products: bool = False) -> dict:
        returning_dict = {
            "commercial_activity_id": self.commercial_activity_id,
            "name": self.name,
            "address": self.address,
            "position_lat": self.position_lat,
            "position_lon": self.position_lon,
            "queue_time": self.queue_time,
        }
        if include_products:
            returning_dict["products"] = [p.serialize(include_availability=True) for p in self.products]
        return returning_dict

    def __repr__(self):
        return '<CommercialActivity id {}>'.format(self.id)
