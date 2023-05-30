# A simple flights status app

### Using Python, Flask, SQLAlchemy, SQLite

**Instructions to run:**

1. run "FLASK_APP=app FLASK_DEBUG=1 flask run" - which will also create the DB
2. install the requirements, for example through pip install -r requirements.txt

In both cases:
1. the server will expose the functions in port 5000.
2. the functions exposed are:
- /upload (post - should have a .csv file in form-data under "file" key)
- /flights/airline_flight_id (get)

Implementation note:
In a more complex or big project:
- it should have better separation (controller, db calls, business logic). </br>
Being the project so simple, I preferred to do it this way in order to not over-complicate it. 
Having a multiplicity of short files makes it harder to understand.</br>
- it should have a more robust error handling (This solution doesn't support uploading the file several times, it will raise ugly errors if passing the wrong file, etc)

Enjoy. Any comment will be welcomed.