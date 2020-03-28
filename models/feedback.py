import enum
import json
import datetime
from dataclasses import dataclass
from typing import List

from app import db


class FeedbackType(enum.Enum):
    low_availability = 0
    no_availability = 1
    queue_awaiting = 2


@dataclass
class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id: int = db.Column(db.Integer, primary_key=True)
    feedback_type: FeedbackType = db.Column(db.Enum(FeedbackType))
    feedback_value: str = db.Column(db.String(), nullable=True)
    feedback_timestamp: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    comment: str = db.Column(db.String(), nullable=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    product_id: int = db.Column(db.Integer, db.ForeignKey('product.product_id'))

    user: List[dict] = db.relationship("User", uselist=False)
    product: List[dict] = db.relationship("Product", uselist=False)

    def __init__(
        self,
        feedback_type,
        feedback_value,
        feedback_timestamp=datetime.datetime.utcnow(),
        comment=None,
        user_id=None,
        product_id=None
    ):
        self.feedback_type = feedback_type
        self.feedback_value = feedback_value
        self.feedback_timestamp = feedback_timestamp
        self.comment = comment
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return '<Feedback id {}>'.format(self.id)
