import enum
import json

from app import db


class FeedbackType(enum.Enum):
    low_availability = 0
    no_availability = 1
    queue_awaiting = 2


class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True)
    feedback_type = db.Column(db.Enum(FeedbackType))
    feedback_value = db.Column(db.String(), nullable=True)
    comment = db.Column(db.String(), nullable=True)

    def __init__(
        self,
        feedback_type,
        feedback_value
    ):
        self.feedback_type = feedback_type
        self.feedback_value = feedback_value

    def __repr__(self):
        return '<Feedback id {}>'.format(self.id)

    def to_json(self) -> str:
        return (
            json.dumps(
                self,
                cls=[],
                check_circular=False
            )
        )
