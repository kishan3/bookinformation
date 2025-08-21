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
- Filtering and searching capabilities by name, country, publisher, and release date
- Automated tests and code coverage

## API Endpoints

### Books API
- `GET /api/v1/books/` - List all books (supports filtering)
- `POST /api/v1/books/` - Create a new book
- `GET /api/v1/books/{id}/` - Retrieve a specific book
- `PUT /api/v1/books/{id}/` - Update a specific book
- `DELETE /api/v1/books/{id}/` - Delete a specific book

### External Books API
- `GET /api/external-books?name={book_name}` - Fetch book details from "An API of Ice and Fire"

### Filtering Options
Books can be filtered using query parameters:
- `name` - Filter by book name
- `country` - Filter by country
- `publisher` - Filter by publisher
- `release_date` - Filter by release year

Example: `GET /api/v1/books/?country=United%20States&release_date=1996`

---

## Project setup

1. `git clone https://github.com/kishan3/bookinformation.git` and `cd <project_directory>`

2. `./project_setup.sh`

3. `source venv/bin/activate`

4. `pip install -r requirements.txt`

5. `./manage.py migrate`

###### Note: After Installing pytest-django, pytest-cov, mixer 
###### it requires to deactivate and reactivate virtualenv to avoid errors..

## Run Tests
`py.test`

## Runserver

`./runserver.sh`