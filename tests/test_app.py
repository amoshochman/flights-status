from io import BytesIO
from app import create_app
import os
import json


def test_app(tmpdir):
    os.environ['FLIGHTS_DB'] = str(os.path.join(tmpdir, "test.db"))
    print(os.environ['FLIGHTS_DB'])
    web = create_app().test_client()
    filepath = "flights.csv"
    with open(filepath, "rb") as fh:
        buf = BytesIO(fh.read())
        expected_data = dict(file=(buf, "test_flights.csv"), )
    response = web.post('/upload', content_type='multipart/form-data', data=expected_data)
    assert response.status_code == 200
    with open('expected_responses.json') as json_file:
        expected_data = json.load(json_file)['responses']
    flight_id = 'G88'
    response = web.get('flights/' + flight_id)
    assert response.status_code == 200
    assert all(x == y for x, y in zip(json.loads(response.data), [elem for elem in expected_data if elem['airline_flight_id'] == flight_id]))
    flight_id = 'C124'
    response = web.get('flights/' + flight_id)
    assert response.status_code == 200
    assert all(x == y for x, y in zip(json.loads(response.data), [elem for elem in expected_data if elem['airline_flight_id'] == flight_id]))
    response = web.get('flights/some_bad_code')
    assert response.status_code == 200
    assert json.loads(response.data) == []