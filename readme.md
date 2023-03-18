# A simple delivery API

### Using Python, Flask, SQLAlchemy, SQLite, Marshmallow

**Instructions to run:**

Git clone your project locally and then create a file called ".env" on the top level of the project including only the line:

GEO_APIFY_KEY=<your personal key achieved in https://www.geoapify.com/>


If running locally:

1. run "python initialization.py", which will create and populate the DB
2. run "flask run"

If running on Docker: choose some name X and then

1. docker build -t X .     
2. sudo docker run -it -p 5000:5000 -d X  

In both cases the server will expose the functions in port 5000.