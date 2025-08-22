# Book Information REST API Backend

## Overview

This project is a comprehensive RESTful API backend designed for managing book and author information. Built with Django and Django REST Framework, it provides a robust platform for cataloging books with detailed metadata including authors, publication information, and bibliographic details.

### Purpose

The API serves as a digital library management system that enables:
- **Book Catalog Management**: Store and manage comprehensive book information including titles, ISBNs, publication details, and page counts
- **Author Management**: Maintain author records with support for multiple authors per book through many-to-many relationships
- **External Data Integration**: Seamlessly fetch book data from "An API of Ice and Fire" (a popular fantasy book API) to enrich your catalog
- **Advanced Filtering**: Query books by various criteria including name, country, publisher, and release date
- **RESTful Interface**: Full CRUD operations through a clean, standards-compliant REST API

### Use Cases

- Library management systems
- Bookstore inventory management
- Reading list applications
- Book recommendation services
- Academic research databases

## Technical Stack

### Core Framework
- **Backend Framework:** Django 2.2 - A high-level Python web framework for rapid development
- **API Framework:** Django REST Framework - Powerful toolkit for building Web APIs
- **Database:** SQLite (default) - Lightweight database, easily configurable for PostgreSQL, MySQL, etc.

### Key Libraries
- **Filtering:** django-filter - Dynamic filtering of querysets for REST API endpoints
- **HTTP Client:** requests - For making HTTP requests to external APIs
- **Data Generation:** Faker - Generate fake data for testing and development

### Development & Testing
- **Testing Framework:** pytest, pytest-django - Modern testing framework with Django integration
- **Test Coverage:** pytest-cov - Code coverage reporting for tests
- **Test Data:** mixer - Object generation library for testing
- **Type Checking:** mypy, django-stubs - Static type checking for Python code

### Development Environment
- **Python Version:** Python 3.x (recommended 3.7+)
- **Virtual Environment:** virtualenv - Isolated Python environment
- **Package Management:** pip - Python package installer

## Features

- **CRUD Operations**: Complete Create, Read, Update, Delete operations for books and authors
- **Many-to-Many Relationships**: Support for multiple authors per book with proper relational mapping
- **External API Integration**: Fetch book details from "An API of Ice and Fire" external API
- **Advanced Filtering**: Filter and search books by name, country, publisher, and release date
- **Automated Testing**: Comprehensive test suite with code coverage reporting
- **Type Safety**: Static type checking with mypy for improved code quality
- **RESTful Design**: Standards-compliant REST API with proper HTTP status codes

## Data Models

### Book Model
The core entity representing a book with the following attributes:
- **name**: Book title (CharField, max 256 characters)
- **isbn**: International Standard Book Number (CharField, max 14 characters)
- **country**: Country of publication (CharField, max 256 characters)
- **authors**: Many-to-many relationship with Author model
- **number_of_pages**: Page count (IntegerField)
- **publisher**: Publishing house (CharField, max 256 characters)
- **release_date**: Publication date (DateField)

### Author Model
Represents book authors with:
- **name**: Author's full name (CharField, max 256 characters, primary key)

### Relationships
- **Book ↔ Author**: Many-to-many relationship allowing multiple authors per book and multiple books per author

## API Endpoints

### Books API
- `GET /api/v1/books/` - List all books (supports filtering)
- `POST /api/v1/books/` - Create a new book
- `GET /api/v1/books/{id}/` - Retrieve a specific book
- `PUT /api/v1/books/{id}/` - Update a specific book
- `DELETE /api/v1/books/{id}/` - Delete a specific book

### External Books API
- `GET /api/external-books?name={book_name}` - Fetch book details from "An API of Ice and Fire"

### Example API Usage

#### Create a New Book
```bash
POST /api/v1/books/
Content-Type: application/json

{
    "name": "A Game of Thrones",
    "isbn": "978-0553103540",
    "country": "United States",
    "authors": ["George R. R. Martin"],
    "number_of_pages": 694,
    "publisher": "Bantam Books",
    "release_date": "1996-08-01"
}
```

**Response:**
```json
{
    "status_code": 201,
    "status": "success",
    "data": [{
        "book": {
            "id": 1,
            "name": "A Game of Thrones",
            "isbn": "978-0553103540",
            "country": "United States",
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "release_date": "1996-08-01",
            "authors": ["George R. R. Martin"]
        }
    }]
}
```

#### Retrieve Books List
```bash
GET /api/v1/books/
```

**Response:**
```json
{
    "status_code": 200,
    "status": "success",
    "data": [
        {
            "id": 1,
            "name": "A Game of Thrones",
            "isbn": "978-0553103540",
            "country": "United States",
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "release_date": "1996-08-01",
            "authors": ["George R. R. Martin"]
        }
    ]
}
```

#### Fetch from External API
```bash
GET /api/external-books?name=A Game of Thrones
```

**Response:**
```json
{
    "status_code": 200,
    "status": "success",
    "data": [
        {
            "name": "A Game of Thrones",
            "isbn": "978-0553103540",
            "authors": ["George R. R. Martin"],
            "numberOfPages": 694,
            "publisher": "Bantam Books",
            "country": "United States",
            "release_date": "1996-08-01"
        }
    ]
}
```

### Filtering Options
Books can be filtered using query parameters:
- `name` - Filter by book name (partial match)
- `country` - Filter by country of publication
- `publisher` - Filter by publisher name
- `release_date` - Filter by release year

**Examples:**
- `GET /api/v1/books/?country=United%20States&release_date=1996`
- `GET /api/v1/books/?name=Game&publisher=Bantam`
- `GET /api/v1/books/?country=United%20States`

---

## Project Structure

```
bookinformation/
├── bookinformation/          # Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── test_settings.py     # Test-specific settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── book/                     # Main application
│   ├── migrations/          # Database migrations
│   ├── tests/               # Test files
│   │   ├── dummy_data.py    # Test fixtures
│   │   ├── test_models.py   # Model tests
│   │   └── test_views.py    # API endpoint tests
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── constants.py         # Application constants
│   ├── models.py            # Data models (Book, Author)
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL patterns
│   └── views.py             # API views and logic
├── manage.py                # Django management script
├── project_setup.sh         # Environment setup script
├── requirements.txt         # Python dependencies
├── runserver.sh             # Development server launcher
├── pytest.ini              # Pytest configuration
├── tox.ini                  # Tox configuration
└── README.md                # Project documentation
```

## Project setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Git
- SQLite3 (usually pre-installed with Python)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/kishan3/bookinformation.git
   cd bookinformation
   ```

2. **Set up the development environment**
   ```bash
   ./project_setup.sh
   ```
   This script will:
   - Update system packages
   - Install Python 3 and pip
   - Install SQLite development libraries
   - Create a Python virtual environment

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database**
   ```bash
   ./manage.py migrate
   ```
   This creates the SQLite database and applies all migrations.

6. **Verify installation**
   ```bash
   ./manage.py check
   ```

### Important Notes
- After installing pytest-django, pytest-cov, and mixer, you may need to deactivate and reactivate the virtual environment to avoid import errors
- The default database is SQLite, which is suitable for development. For production, consider PostgreSQL or MySQL

## Development

### Running Tests
Execute the test suite to ensure everything is working correctly:
```bash
# Run all tests
py.test

# Run tests with coverage report
py.test --cov=book

# Run specific test file
py.test book/tests/test_models.py

# Run tests verbosely
py.test -v
```

### Running the Development Server
Start the Django development server:
```bash
# Using the provided script (runs on 0.0.0.0:8080)
./runserver.sh

# Or using Django's manage.py directly (runs on 127.0.0.1:8000)
./manage.py runserver
```

The API will be available at:
- `http://localhost:8080` (using runserver.sh)
- `http://127.0.0.1:8000` (using manage.py)

### API Documentation
Once the server is running, you can explore the API:
- Visit `/api/v1/books/` for the books API
- Visit `/api/external-books?name=example` for external API integration
- Use tools like Postman, curl, or httpie to test the endpoints

## External API Integration

### An API of Ice and Fire
This project integrates with [An API of Ice and Fire](https://anapioficeandfire.com/), which provides data about the book series "A Song of Ice and Fire" by George R. R. Martin.

**Features:**
- Fetch book information by name
- Automatic data transformation to match internal API format
- Error handling for network issues and API failures
- Response caching capabilities

**Data Transformation:**
The external API response is automatically processed to:
- Remove unnecessary fields (`url`, `mediaType`, `characters`, `povCharacters`)
- Convert `released` timestamp to `release_date` format
- Maintain consistency with internal data structure

**Example Integration:**
```bash
# Fetch "A Game of Thrones" from external API
curl "http://localhost:8080/api/external-books?name=A Game of Thrones"
```

## Troubleshooting

### Common Issues

1. **Import Errors After Installing Dependencies**
   ```bash
   # Solution: Deactivate and reactivate virtual environment
   deactivate
   source venv/bin/activate
   ```

2. **Database Migration Errors**
   ```bash
   # Check migration status
   ./manage.py showmigrations
   
   # Apply migrations
   ./manage.py migrate
   
   # Reset database (development only)
   rm db.sqlite3
   ./manage.py migrate
   ```

3. **External API Connection Issues**
   - Check internet connectivity
   - Verify the external API is accessible: https://anapioficeandfire.com/api/books
   - Review error messages in the API response

4. **Testing Issues**
   ```bash
   # Clear pytest cache
   py.test --cache-clear
   
   # Run tests without coverage for faster execution
   py.test --no-cov
   ```

### Development Guidelines

#### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate (mypy configuration included)
- Write descriptive commit messages
- Keep functions and classes focused and small

#### Testing
- Write tests for all new features
- Maintain high test coverage (aim for >90%)
- Use pytest fixtures for test data
- Mock external API calls in tests

#### Database
- Always create migrations for model changes: `./manage.py makemigrations`
- Test migrations on a copy of production data
- Use descriptive migration names

#### API Design
- Follow REST conventions
- Use proper HTTP status codes
- Provide consistent error response formats
- Document new endpoints with examples

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `py.test`
5. Commit your changes: `git commit -m "Add feature"`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is open source. Please check with the repository owner for specific license terms.