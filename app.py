import pandas as pd
from flask import Flask, request, Response
import logging
import os
from models import db, Flight
from datetime import timedelta
from werkzeug.utils import secure_filename

MAX_SUCCESS_PER_DAY = 20
MIN_HOUR_DIFF = 3

FLIGHT_ID = 'flight ID'
ARRIVAL = 'Arrival'
DEPARTURE = 'Departure'
SUCCESS = 'success'
FAIL = 'fail'
TIME_FORMAT = "%H:%M:%S"


def as_dict(my_object):
    return {c.name: getattr(my_object, c.name) for c in my_object.__table__.columns}


def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)

    with app.app_context():
        db_file = os.environ.get('FLIGHTS_DB') or 'flights.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        db.create_all()

        @app.get('/flights/<string:airline_flight_id>')
        def get_flight(airline_flight_id):
            return [as_dict(flight) for flight in Flight.query.filter_by(airline_flight_id=airline_flight_id).all()]

        def update_db(df):
            df.columns = df.columns.str.strip()
            try:
                df.Arrival = pd.to_datetime(df.Arrival.str.strip())
                df.Departure = pd.to_datetime(df.Departure.str.strip())
            except pd._libs.tslibs.parsing.DateParseError:
                return Response("invalid time format", status=400)
            df.sort_values(by=ARRIVAL, inplace=True)
            success_total = Flight.query.filter_by(success=SUCCESS).count()
            for index, row in df.iterrows():
                new_flight = Flight(row[FLIGHT_ID], row[ARRIVAL].strftime(TIME_FORMAT),
                                    row[DEPARTURE].strftime(TIME_FORMAT))
                if success_total >= MAX_SUCCESS_PER_DAY:
                    new_flight.success = FAIL
                else:
                    time_diff_big_enough = (row.Departure - row.Arrival) >= timedelta(hours=MIN_HOUR_DIFF)
                    if time_diff_big_enough:
                        new_flight.success = SUCCESS
                        success_total += 1
                    else:
                        new_flight.success = FAIL
                db.session.add(new_flight)
            db.session.commit()
            return "upload done successfully"

        @app.route('/upload', methods=['POST'])
        def upload():
            f = request.files.get('file')
            if not f:
                error = "file not provided"
                return Response(error, status=400)
            name = f.filename
            extension = os.path.splitext(name)[1]
            if extension != ".csv":
                error = "extension is not csv"
                return Response(error, status=400)
            f.save(secure_filename(name))
            df = pd.read_csv(name)
            os.remove(name)
            return update_db(df)

    return app
