from sqlalchemy import exc

from app import app, db, Timeslot
import json
from datetime import datetime



def insert_timeslots(timeslot):
    for code in timeslot['supported_postcodes']:
        start = datetime.strptime(timeslot['start_time'], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(timeslot['end_time'], '%Y-%m-%d %H:%M:%S')
        new_timeslot = Timeslot(start, end, code)
        db.session.add(new_timeslot)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()

with app.app_context():
    db.create_all()
    with open("initial_data/Timeslots.json") as file:
        initial_timeslots = json.load(file)['courier_available_timeslots']
        for timeslot in initial_timeslots:
            insert_timeslots(timeslot)