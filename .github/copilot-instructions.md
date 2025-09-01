# Book Information REST API Backend

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup
- Run system setup: `./project_setup.sh` -- takes 12 seconds. Install Python 3, pip, SQLite, and create virtualenv.
- Install system dependencies: `sudo apt-get install -y python3-django python3-djangorestframework python3-requests python3-django-filters python3-pytest python3-pytest-django python3-flake8`
- **CRITICAL**: Do NOT use `pip install -r requirements.txt` - it fails due to network timeouts and Python 3.12 compatibility issues with Django 2.2.
- Use system Django 4.2.11 instead of requirements.txt Django 2.2.24 - both work with this codebase.

### Database Setup
- Run migrations: `PYTHONPATH=/usr/lib/python3/dist-packages python3 manage.py migrate` -- takes less than 1 second.
- Database uses SQLite and is created automatically.

### Development Server
- Start server: `PYTHONPATH=/usr/lib/python3/dist-packages python3 manage.py runserver 0.0.0.0:8080`
- Server runs on http://localhost:8080 and starts immediately.
- **NEVER CANCEL**: Server runs indefinitely until stopped with Ctrl+C.

### Testing
- Run view tests only: `cd /home/runner/work/bookinformation/bookinformation && mv pytest.ini pytest.ini.bak && cd /tmp && PYTHONPATH=/usr/lib/python3/dist-packages:/home/runner/work/bookinformation/bookinformation DJANGO_SETTINGS_MODULE=bookinformation.test_settings python3 -m pytest -v --nomigrations /home/runner/work/bookinformation/bookinformation/book/tests/test_views.py && cd /home/runner/work/bookinformation/bookinformation && mv pytest.ini.bak pytest.ini` -- takes 0.8 seconds for 11 tests.
- **WARNING**: pytest.ini contains coverage options that fail with system pytest. Temporarily rename pytest.ini to avoid config conflicts.
- **WARNING**: Model and serializer tests require 'mixer' package which has installation issues. Skip them by running view tests only.
- **NEVER CANCEL**: Tests complete in under 1 second. Set timeout to 5+ minutes to be safe.

### Code Quality
- Run linting: `python3 -m flake8 --config=tox.ini .` -- takes 0.2 seconds.
- Linting finds minor issues in test_settings.py (F403, F401) - these are expected and can be ignored.
- Type checking available via mypy but not configured in this project.

## Validation

Always manually validate any new code via the following scenarios:

### Complete End-to-End API Testing Scenario
1. Start the development server
2. Test book listing: `curl -s http://localhost:8080/api/v1/books/`
3. Create a book: `curl -X POST http://localhost:8080/api/v1/books/ -H "Content-Type: application/json" -d '{"name":"Test Book","isbn":"123-456789012","country":"USA","number_of_pages":100,"publisher":"Test Publisher","release_date":"2023-01-01","authors":["Test Author"]}'`
4. Verify book creation returned status 201 and proper JSON response
5. Test book retrieval: `curl -s http://localhost:8080/api/v1/books/1/`
6. Test external API (will return internet error in restricted environments): `curl -s "http://localhost:8080/api/external-books?name=A%20Game%20of%20Thrones"`

### Filtering and Search Testing
- Test filtering by country: `curl -s "http://localhost:8080/api/v1/books/?country=USA"`
- Test filtering by year: `curl -s "http://localhost:8080/api/v1/books/?release_date=2023"`
- Test filtering by name: `curl -s "http://localhost:8080/api/v1/books/?name=Test"`

### Always run these commands before finishing
- `python3 -m flake8 --config=tox.ini .` -- ensure code quality
- `mv pytest.ini pytest.ini.bak && cd /tmp && PYTHONPATH=/usr/lib/python3/dist-packages:/home/runner/work/bookinformation/bookinformation DJANGO_SETTINGS_MODULE=bookinformation.test_settings python3 -m pytest -v --nomigrations /home/runner/work/bookinformation/bookinformation/book/tests/test_views.py && cd /home/runner/work/bookinformation/bookinformation && mv pytest.ini.bak pytest.ini` -- ensure tests pass

## Common Tasks

### Repository Structure
```
.
├── README.md                   # Project documentation
├── manage.py                   # Django management script  
├── project_setup.sh            # System setup script
├── runserver.sh               # Django server startup script
├── requirements.txt           # Python dependencies (DO NOT USE - has compatibility issues)
├── pytest.ini                # Test configuration (has coverage options that fail)
├── tox.ini                    # Flake8 linting configuration
├── .coveragerc               # Coverage configuration
├── bookinformation/          # Django project settings
│   ├── settings.py           # Main settings
│   ├── test_settings.py      # Test settings (uses in-memory SQLite)
│   └── urls.py               # URL routing
└── book/                     # Main Django app
    ├── models.py             # Book and Author models
    ├── views.py              # API views and external API integration
    ├── serializers.py        # DRF serializers
    ├── urls.py               # App URL routing
    ├── constants.py          # Status codes and field exclusions
    └── tests/               # Test files
        ├── test_views.py     # API view tests (WORKS)
        ├── test_models.py    # Model tests (requires mixer - SKIP)
        └── test_serializers.py # Serializer tests (requires mixer - SKIP)
```

### Key API Endpoints
- `GET /api/v1/books/` - List all books (supports filtering)
- `POST /api/v1/books/` - Create a new book
- `GET /api/v1/books/{id}/` - Retrieve a specific book
- `PUT /api/v1/books/{id}/` - Update a specific book  
- `DELETE /api/v1/books/{id}/` - Delete a specific book
- `GET /api/external-books?name={book_name}` - Fetch from external "An API of Ice and Fire" API

### Dependencies and Known Issues
- **System Django 4.2.11 works** - Use instead of requirements.txt Django 2.2.24
- **pip install requirements.txt FAILS** - Network timeouts and Python 3.12 compatibility issues
- **External API requires internet** - Returns "You are not connected to internet!" in restricted environments
- **Tests need mixer package** - Skip model/serializer tests, run view tests only
- **Coverage tools not available** - Run pytest without --cov options

### Environment Variables and Paths
- Always use: `PYTHONPATH=/usr/lib/python3/dist-packages` for system packages
- Test settings: `DJANGO_SETTINGS_MODULE=bookinformation.test_settings`
- Server runs on: `0.0.0.0:8080`

### Performance Expectations
- **Project setup: 12 seconds** - System package installation
- **Migrations: < 1 second** - SQLite database creation
- **Server startup: Immediate** - Ready in under 1 second
- **Tests: 0.8 seconds** - 11 view tests complete quickly
- **Linting: 0.2 seconds** - Fast flake8 execution

## Critical Warnings
- **NEVER use pip install -r requirements.txt** - Always use system packages
- **NEVER try to run model/serializer tests** - They require unavailable mixer package
- **ALWAYS use PYTHONPATH=/usr/lib/python3/dist-packages** - Required for system Django
- **ALWAYS test API functionality manually** - Unit tests alone are insufficient validation