import enum

from app import db


class OfferType(enum.Enum):
    availability = 0
    no_availability = 1
    queue_awaiting = 3


class Offer(db.Model):
    __tablename__ = "offer"

    offer_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    commercial_activity_id = db.Column(db.Integer, db.ForeignKey('commercial_activity.commercial_activity_id'))
    availability = db.Column(db.Float)
    product = db.relationship("Product", uselist=False)
    commercial_activity = db.relationship("CommercialActivity", uselist=False)

    def __init__(
        self,
        product_id: int,
        commercial_activity_id: int,
        availability: float,
        offer_id: int = None
    ):
        self.product_id = product_id
        self.commercial_activity_id = commercial_activity_id
        self.availability = availability
        self.offer_id = offer_id

    def __repr__(self):
        return (
            "<Offer id Commercial activity {} offers prduct {}>".format(
                self.offer_id,
                self.commercial_activity_id,
                self.product_id
            )
        )
