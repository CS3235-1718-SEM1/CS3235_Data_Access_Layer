# CS3235_Data_Access_Layer
Data Access Layer is a Python Flask application that abstracts database accesses by exposing a RESTful API

## Dependencies
Please refer to the Pipfile for a complete list of latest dependencies.

## Development
1. Install `Python 3.5, PostgreSQL, pipenv`
2. Install all the project dependencies by executing `pipenv install`
3. Setup your DB URL through the environment variable `DATABASE_URL`. For example: `DATABASE_URL=postgres:///cs3235`
4. Using `flask-migrate`, initialize the DB
5. Populate the DB with static data such as module list, etc using the `/dal/models/db_population.py` script.
