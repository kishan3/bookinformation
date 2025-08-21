# Book Information REST API Backend

This project is a RESTful API backend for managing book and author information. It is built using Django and Django REST Framework. The API allows users to perform CRUD operations on books and authors, and also provides integration with the external "An API of Ice and Fire" to fetch book details.

## Technical Stack

- **Backend Framework:** Django 2.2
- **API Framework:** Django REST Framework
- **Database:** SQLite (default, can be changed)
- **Filtering:** django-filter
- **Testing:** pytest, pytest-django, pytest-cov, mixer
- **Type Checking:** mypy, django-stubs
- **Other Libraries:** Faker (for dummy data), requests (for external API calls)

## Features

- CRUD operations for books and authors
- Many-to-many relationship between books and authors
- Fetch book details from the "An API of Ice and Fire" external API
- Filtering and searching capabilities
- Automated tests and code coverage

---

## Project setup

1. `git clone https://github.com/kishan3/bookinformation.git` and `cd <project_directory>`

2. `./project_setup.sh`

3. `source venv/bin/actiave`

4. `pip install -r requirements.txt`

5. `./manage.py migrate`

###### Note: After Installing pytest-django, pytest-cov, mixer 
###### it requires to deactivate and reactivate virtualenv to avoid errors..

## Run Tests
`py.test`

## Runserver

`./runserver.sh`