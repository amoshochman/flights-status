from sqlalchemy import exc

from app import app, db, Timeslot
import json
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'


def insert_timeslots(start, end, codes):
    for code in codes:
        new_timeslot = Timeslot(start, end, code)
        db.session.add(new_timeslot)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()


def timeslot_intersects_holiday(timeslot_start, timeslot_end, holidays):
    return True if (timeslot_start in holidays or timeslot_end in holidays) else False


def get_holidays_dates_from_file():
    with open("initial_data/Holidays.json") as holidays_file:
        holidays_data = json.load(holidays_file)['holidays']
        holidays_dates = {elem['date'] for elem in holidays_data}
        holidays_dates = {datetime.strptime(elem, DATE_FORMAT).date() for elem in holidays_dates}
    return holidays_dates


def get_timeslots_from_file():
    with open("initial_data/Timeslots.json") as timeslots_file:
        initial_timeslots = json.load(timeslots_file)['courier_available_timeslots']
    return initial_timeslots


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        holidays_dates = get_holidays_dates_from_file()
        timeslots = get_timeslots_from_file()
        for timeslot in timeslots:
            datetime_format = DATE_FORMAT + " " + TIME_FORMAT
            start = datetime.strptime(timeslot['start_time'], datetime_format)
            end = datetime.strptime(timeslot['end_time'], datetime_format)
            if timeslot_intersects_holiday(start.date(), end.date(), holidays_dates):
                continue
            insert_timeslots(start, end, timeslot['supported_postcodes'])
