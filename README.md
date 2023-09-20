# Customer Order API

[![Build Status](https://travis-ci.org/yourusername/yourproject.svg?branch=master)](https://travis-ci.org/owinoBen/yourproject)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

This is a Django Rest Framework (DRF) project that provides a customer with a platform to register, get authenticated and place an order.

## Features

- Register customer
- Oauth2 authentication
- Sends sms after successful registration
- Update or delete customer information 
- customer can place order and receive a confirmation message after successfully order placement
- Customers can update orders
- [List the key features and functionalities of your project]

## Requirements

- Python (>= 3.10)
- Django (>= 4.2.5)
- Django Rest Framework (>= 3.14.0)
- africastalking (>=1.2.5)
- django-oauth-toolkit (>=2.3.0)
- django-celery-beat (>=2.5.0)
- celery (>=5.3.4)
- django-cors-headers (>=4.2.0)
- gunicorn (>=21.2.0)
- Pillow (>=10.0.0)
- psycopg2-binary (>=2.9.7)
- Docker
- kubernetes
- RabbitMQ

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OwinoBen/savannah-interview.git
2. Navigate to the project directory:
    ``` bash
    cd savannah-interview
    Create a virtual environment (optional but recommended):
    cd savannah-interview
    Create a virtual environment (optional but recommended):
    
    python -m venv venv
    
    Activate the virtual environment:
    source venv/bin/activate
    
    Install the project dependencies:
    pip install -r requirements.txt
    
    Set up the database:
    python manage.py migrate
   
    Create a superuser (admin) account:
    python manage.py createsuperuser
    
    Start the development server:
    python manage.py runserver
    Access the API at http://localhost:8000/

3. Docker and kubernetes
   - Install docker and run:
   ``` docker-compose
   docker-compose -f docker-compose.prod.yml up -d --buid

- Create a .env files with the required variables
## Usage
  1. Customer Operations
      - Create a Customer
      ```bash
      POST /api/customers/
      Content-Type: application/json
    
      {
        "email": "owinoben@gmail.com",
        "password": "123",
        "username": "Bens",
        "first_name":"Benson",
        "last_name":"opondo",
        "phone": "0790232329",
        "confirm_pass": "123"
      }
        response
     HTTP/1.1 201 Created
     Content-Type: application/json

     {
       "errors":fales
        "response: [
            "details":{
                "message": "Account created"
            }
        }
## Testing
 - To run unit test with coverage, run:
    ```bash
    docker-compose -f docker-compose.prod.yml exec web coverage --source=savannah manage.py test

## Acknowledgments

This project is made possible thanks to the fantastic open-source libraries, frameworks, and communities that have contributed to its development. We would like to express our gratitude to:

- [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines.
- [Django Rest Framework](https://www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs in Django.
- [PostgreSQL](https://www.postgresql.org/): An open-source relational database management system.
- [Swagger](https://swagger.io/): Used for creating the interactive API documentation.
- [Circle CI](https://travis-ci.org/): For continuous integration and automated testing.
- [GitHub](https://github.com/): For hosting our project and facilitating collaboration.
- [Docker](https://docker.com/): 
- [AWS](https://github.com/): For hosting our project cotainers and facilitating container management.
- [Django OAuth Toolkit](https://github.com/jazzband/django-oauth-toolkit/blob/13a61435167d8ffe04dd6b79522d5d20007a08c5/docs/index.rst): Django OAuth Toolkit can help you by providing, out of the box, all the endpoints, data, and logic needed to add OAuth2 capabilities to your Django projects


## Author
Benson Opondo  - owinoben2020@gmail.com






