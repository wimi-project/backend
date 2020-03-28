import json

from app import db


class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True)
    product_description = db.Column(db.String(), nullable=False)
    product_image_url = db.Column(db.String())
    commercial_activities = db.relationship("Offer")

    def __init__(
        self,
        product_description,
        product_image_url
    ):
        self.product_description = product_description
        self.product_image_url = product_image_url

    def __repr__(self):
        return "<Product id {}>".format(self.id)

    def to_json(self) -> str:
        return (
            json.dumps(
                self,
                cls=[],
                check_circular=False
            )
        )
