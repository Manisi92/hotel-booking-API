# hotel-booking-API
A FastAPI project for hotel booking management

# hotel-booking-api
A FastAPI project for hotel booking management

Hotel Booking API

This project is a REST API for managing hotel bookings, built with FastAPI. It allows users to register, make room bookings, write reviews, handle payments, and more.
Technologies Used

    FastAPI: Web framework for building fast APIs.
    SQLAlchemy: ORM for interacting with the database.
    PostgreSQL: Relational database for data persistence.
    Uvicorn: ASGI server for running the FastAPI app.
    Pydantic: Used for data validation.
    Alembic: Used for database migrations.
    JWT (JSON Web Token): Authentication via token.

Features

    User registration
    Authentication and role management (Admin, Manager, Guest)
    Room booking creation and management
    Review creation and management
    Payment processing

Project Structure

/hotel_booking_api
  ├── app
  │   ├── main.py            # FastAPI app entry point
  │   ├── models.py          # Database models
  │   ├── schemas.py         # Pydantic schemas for validation and serialization
  │   ├── crud.py            # CRUD functions for interacting with the database
  │   ├── auth.py            # Authentication and token management functions
  │   └── database.py        # Database connection
  ├── requirements.txt       # Project dependencies
  └── alembic.ini            # Alembic configuration for migrations

Requirements

    Python 3.8+
    PostgreSQL or another supported relational database
    pip for managing dependencies

Installation

Follow these steps to set up the development environment:

    Clone the repository:

git clone https://github.com/your-username/hotel-booking-api.git
cd hotel-booking-api

Create and activate a virtual environment:

    On Windows:

python -m venv venv
.\venv\Scripts\activate

On Linux/macOS:

    python3 -m venv venv
    source venv/bin/activate

Install the dependencies:

pip install -r requirements.txt

Set up the database:

    Create a PostgreSQL database (or use another supported database).
    Update the database connection configuration in app/database.py (modify the connection string if necessary).

Run the database migrations:

After setting up the database, run the migrations with Alembic:

alembic upgrade head

Run the app:

Once the environment is set up, start the server using Uvicorn:

    uvicorn app.main:app --reload

    The app will be available at: http://127.0.0.1:8000

Usage
Main Endpoints

    POST /users/register: Register a new user (requires username, email, and password).
    POST /users/login: Authenticate a user and return a JWT for future requests.
    GET /rooms: Get a list of available rooms.
    POST /bookings: Create a booking.
    GET /reviews: View reviews.
    POST /payments: Process payment for a booking.

Authentication

To access protected resources, include the JWT in the header of your requests as follows:

Authorization: Bearer <your_jwt_token>

Example of a registration request:

curl -X 'POST' \
  'http://127.0.0.1:8000/users/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secretpassword"
}'

Example of a login request:

curl -X 'POST' \
  'http://127.0.0.1:8000/users/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "john_doe",
  "password": "secretpassword"
}'

The response will contain a JWT that you will use for future requests.
Testing

The tests for the project are written with pytest. To run the tests, use the following command:

pytest

Migrations

Database migrations are handled with Alembic. To create a new migration, run:

alembic revision --autogenerate -m "Migration description"

To apply the migrations to the database, run:

alembic upgrade head

Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

    Fork this repository
    Create a new branch (git checkout -b feature-name)
    Commit your changes (git commit -am 'Add a new feature')
    Push the branch (git push origin feature-name)
    Create a pull request

License

This project is licensed under the MIT License. See the LICENSE file for more details.
