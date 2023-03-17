from models import Timeslot, Delivery
from sqlalchemy import func


class InvalidTimeSlotException(Exception):
    pass


def get_deliveries_num_per_date(date):
    return Delivery.query.join(Timeslot).filter(func.date(Timeslot.start_time) == date).count()


def get_date_for_timeslot(timeslot_id):
    timeslot = Timeslot.query.get(timeslot_id)
    if not timeslot:
        raise InvalidTimeSlotException
    return timeslot.start_time.date()


def get_deliveries_num_per_timeslot(timeslot_id):
    return Delivery.query.filter(Delivery.timeslot_id == timeslot_id).count()
