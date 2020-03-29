import json
from dataclasses import dataclass

from sqlalchemy.orm import relationship

from app import db
from utils.enums import Availability

from typing import Optional


@dataclass
class Product(db.Model):
    __tablename__ = 'product'

    product_id: int = db.Column(db.Integer, primary_key=True)
    product_name: str = db.Column(db.String(), nullable=False, unique=True)
    product_description: str = db.Column(db.String(), nullable=False)
    product_image_url: str = db.Column(db.String())
    feedbacks = relationship("Feedback")
    present_in = db.relationship(
        "CommercialActivity",
        secondary="offer"
    )
    availability: Optional[Availability] = None

    def __init__(
        self,
        product_name,
        product_description,
        product_image_url=None,
        product_id=None
    ):
        self.product_name = product_name
        self.product_description = product_description
        self.product_image_url = product_image_url
        self.product_id = product_id

    def __repr__(self):
        return "<Product id {} named {}>".format(self.id, self.product_name)

    def serialize(self, include_feedbacks: bool = False, include_availability: bool = False) -> dict:
        serialized_dict = (
            {
                "product_id": self.product_id,
                "product_name": self.product_name,
                "product_description": self.product_description,
                "product_image_url": self.product_image_url,
            }
        )
        if include_feedbacks:
            serialized_dict["feedbacks"] = self.feedbacks
        if include_availability:
            serialized_dict["availability"] = self.availability.name
        return serialized_dict
