from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline_flight_id = db.Column(db.String)
    arrival = db.Column(db.String)
    departure = db.Column(db.String)
    success = db.Column(db.String)

    def __init__(self, airline_flight_id, arrival, departure):
        self.airline_flight_id = airline_flight_id
        self.arrival = arrival
        self.departure = departure
