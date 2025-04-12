# SWAPI Planets API

A Django-based REST API for managing Star Wars planet data.

## Overview

This project imports planet data from the [SWAPI GraphQL API](https://swapi-graphql.netlify.app/graphql) and provides a full CRUD API for managing planets using Django REST Framework. It also includes robust error handling, logging, and comprehensive tests.

## Features

- **Data Import:** Fetches and stores planet data from a GraphQL endpoint.
- **CRUD Endpoints:** Provides create, read, update, and delete operations for planet data.
- **Error Handling & Logging:** Enhanced error handling in the management command and API views, with logging support.
- **Testing:** Unit and integration tests for models, API endpoints, and the import command.
- **Browsable API:** Leverages Django REST Framework’s browsable API for easy testing and development.
- **Comprehensive Documentation:** This README provides detailed instructions on setup, usage, and testing.

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- (Optional) Virtual Environment tool (e.g., `venv`)

### Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd swapi_project
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On macOS/Linux
   venv\Scripts\activate         # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   If a `requirements.txt` file is not present, install the required packages directly:
   ```bash
   pip install django djangorestframework requests
   ```

4. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for Django admin access):**
   ```bash
   python manage.py createsuperuser
   ```

### Importing Data

To fetch and import planet data from the SWAPI GraphQL endpoint, run the custom management command:

```bash
python manage.py import_planets
```

This command:
- Queries the SWAPI GraphQL API.
- Handles errors with logging.
- Imports or updates planet records in the database.

### Running the Development Server

Start the Django server:

```bash
python manage.py runserver
```

### Accessing the Application

- **Admin Panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **API Endpoints:**
  - List/Create Planets: [http://127.0.0.1:8000/api/planets/](http://127.0.0.1:8000/api/planets/)
  - Detail/Update/Delete Planet: [http://127.0.0.1:8000/api/planets/<id>/](http://127.0.0.1:8000/api/planets/<id>/)

### API Usage Examples

#### GET All Planets
```bash
curl -X GET http://127.0.0.1:8000/api/planets/
```

#### GET a Single Planet
```bash
curl -X GET http://127.0.0.1:8000/api/planets/1/
```

#### Create a New Planet
```bash
curl -X POST http://127.0.0.1:8000/api/planets/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Kamino", "population": "1000000", "terrains": "ocean", "climates": "rainy"}'
```

#### Update a Planet (PUT)
```bash
curl -X PUT http://127.0.0.1:8000/api/planets/1/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Kamino Updated", "population": "2000000", "terrains": "ocean", "climates": "rainy"}'
```

#### Partial Update (PATCH)
```bash
curl -X PATCH http://127.0.0.1:8000/api/planets/1/ \
     -H "Content-Type: application/json" \
     -d '{"population": "3000000"}'
```

#### Delete a Planet
```bash
curl -X DELETE http://127.0.0.1:8000/api/planets/1/
```

## Testing

Run the unit and integration tests using:

```bash
python manage.py test
```

To check test coverage, install and run coverage:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

Your current test coverage is around 93%, ensuring a robust codebase.

## Error Handling & Logging

### Error Handling

- **Management Command:**  
  The command `import_planets` uses `try/except` blocks to catch errors when fetching or parsing data from the SWAPI GraphQL API. If any error occurs, a meaningful error message is printed and logged.

- **API Endpoints:**  
  The API endpoints return detailed error messages. A custom exception handler (configured in `swapi_project/settings.py`) adds extra context to API error responses.

### Logging

This project uses Django's built-in logging framework to capture errors and debugging information. Logs are written to both the console and a file (`project.log`) for easy debugging and monitoring. Here's an example configuration:
```python
LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'verbose': {
           'format': '{levelname} {asctime} {module} {message}',
           'style': '{',
       },
   },
   'handlers': {
       'console': {
           'class': 'logging.StreamHandler',
           'formatter': 'verbose',
       },
       'file': {
           'class': 'logging.FileHandler',
           'filename': 'project.log',
           'formatter': 'verbose',
       },
   },
   'loggers': {
       '': {
           'handlers': ['console', 'file'],
           'level': 'DEBUG',
       },
   },
}
```