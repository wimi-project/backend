import json

from app import db
from dataclasses import dataclass
from typing import List
from sqlalchemy.orm import relationship


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

    def to_json(self) -> str:
        return (
            json.dumps(
                self,
                cls=[],
                check_circular=False
            )
        )
