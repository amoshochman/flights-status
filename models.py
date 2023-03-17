from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


def as_dict(my_object):
    return {c.name: getattr(my_object, c.name) for c in my_object.__table__.columns}

class Timeslot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    postcode = db.Column(db.Integer)
    UniqueConstraint(start_time, end_time, postcode, name="uix_1")

    def __init__(self, start_time, end_time, postcode):
        self.start_time = start_time
        self.end_time = end_time
        self.postcode = postcode


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    status = db.Column(db.String)
    timeslot_id = db.Column(db.Integer, ForeignKey(Timeslot.id))
    timeslot = relationship("Timeslot", backref="parents")

    def __init__(self, user_id, timeslot_id, status="booked"):
        self.user_id = user_id
        self.status = status
        self.timeslot_id = timeslot_id


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    line1 = db.Column(db.String)
    line2 = db.Column(db.String)
    country = db.Column(db.String)
    postcode = db.Column(db.Integer)

