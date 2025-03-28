# spotter_trip_planner
- Track trips tracking system.


## What I managed to achieve.
- Route Calculation & ELD Generation: Uses SpotterHelper to compute route stops and generate ELD logs.
- Unit testing.
- Deployment to Vercel.app

&nbsp;

## What I could have done better

- Include user Registration module to associate every route to a user
- Increase my test coverage.
- Deploy by docker container.

&nbsp;

## Prerequisites before you start off the project

### For you to fire up this project locally, you should have the following installed.

- [Python 3.10](https://www.python.org/)
- [Postgres](https://www.postgresql.org/)

&nbsp;

## How to set this manually

- `https://github.com/dunnyk/spotter.git`
- `cd spotter` to navigate to the project folder
- `python3.10 -m virtualenv venv` and `. venv/bin/activate` to create and activate virtual env         respectively.
- `pip install -r requirements.txt` to install the dependencies.
- `touch .env` to create a new env file
- copy and paste the sample env and replace with your actual credentials
- `source .env` to source env variables
- `python manage.py migrate` to apply all the migrations
- `python manage.py runserver` to start the server
- Navigate to `http://127.0.0.1:8000` to visit the site

## Sample env

- export API_KEY=<API_KEY for OpenRouteService free map access key>
- export DEBUG=<make_  true>
- export DB_NAME=<your_db_name>
- export DB_PASS=<your_db_password>
- export DB_HOST=<your_db_host>
- export DB_PORT=<your_db_port>
- export DB_USER=<your_db_user>

Note: There is no space next to '='

## Project Endpoints

- Trip Creation: Accepts trip data and processes it.
- Route Calculation & ELD Generation: Uses SpotterHelper to compute route stops and generate ELD logs.
- Data Storage: Saves trip metadata, fuel/rest stops, and ELD logs.
- Response Handling: Returns aggregated trip data upon creation.
  - API Endpoints `http://127.0.0.1:8000/trip/` as a `POST` request.
