# CMS APIs with Django REST Framework

This project is a CMS (Content Management System) API built with Django REST Framework (DRF). 

## Core Libraries Used

- Python 3.9
- Django 4.2
- Django REST Framework
- SQLite (default)

## Setup Instructions/Commands

1. python3 -m venv env - For setting up virtual environment
2. source env/bin/activate - For entering the virtual environment
3. pip3 install -r requirements.txt - For installing required libraries
4. python3 manage.py makemigrations cms_app - 
5. python3 manage.py migrate -
6. python3 manage.py createsuperuser - If Django admin dashboard is to be used
7. python3 manage.py runserver - Finally, Starting the server for running APIs
8. pytest - For running testcases

## Additional Instructions

- You can test all 12 APIs in cms_app Application in this Project by using Postman Client - [Postman Collection](https://documenter.getpostman.com/view/26009253/2sA3XQhhhJ)