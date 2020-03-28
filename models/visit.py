from app import db

import datetime


class Visit(db.Model):
    __tablename__ = "visit"

    visit_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    comercial_activity_id = db.Column(db.Integer, db.ForeignKey('commercial_activity.commercial_activity_id'))
    visit_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    user = db.relationship("User", uselist=False)
    commercial_activity = db.relationship("CommercialActivity", uselist=False)

    def __repr__(self):
        return "<Visit id {} by user {}>".format(self.visit_id, self.user_id)
