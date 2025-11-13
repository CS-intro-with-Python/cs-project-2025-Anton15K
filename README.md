[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

## Description

This project is a backend web service that estimates the difficulty rating of Codeforces problems based on the ratings of users who solved them.

Each Codeforces problem is solved by users with varying ratings. By analyzing these solver ratings, the system can estimate a possible difficulty rating for each problem and later adjust it based on user feedback and performance.

The backend is implemented with Flask and exposes a RESTful API for:

- Managing users and authentication
- Managing problems and attempts
- Estimating and updating problem difficulty ratings
- Reporting health status for monitoring

The current repository contains only the backend service; a frontend can be built separately to consume this API.

## Project Structure

```text
Backend/                 # Flask application source code
	app.py                 # Application factory / entry point
	config.py              # Configuration settings
	extensions.py          # Flask extensions initialization
	models.py              # Database models (if using ORM)
	api/                   # REST API blueprints
		auth.py              # Authentication endpoints
		users.py             # User management endpoints
		problems.py          # Problem-related endpoints
		attempts.py          # Attempt-related endpoints
		ratings.py           # Rating adjustment endpoints
		health.py            # Health check endpoint
	entities/              # Domain entities
		user.py
		problem.py
		attempt.py
		rating_adjustment.py
	models/                # Additional models module (if needed)

Dockerfile               # Container image definition for the backend
scripts/
	test_user_requests.py  # Simple script to exercise user-related endpoints
```

## Local Setup

### Prerequisites

- Python 3.10+ (recommended)
- `pip` and `venv`
- (Optional) Docker, if you prefer running the service in a container

### Backend Setup (without Docker)

```bash
# Clone repository
git clone <your-repo-url> && cd cs-project-2025-Anton15K

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # or requirements-dev.txt if present

# Run the Flask app (adjust as needed based on app factory)
cd Backend
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --port 5001
```

Once running, the API should be available at `http://localhost:5001`.

## Running with Docker

The repository includes a `Dockerfile` for building a backend image.

```bash
cd cs-project-2025-Anton15K

# Build the image
docker build -t cs-2025-backend .

# Run the container
docker run --rm -p 5001:5001 cs-2025-backend
```

After the container starts, the API should be accessible at `http://localhost:5001`.

## API Overview

The backend is organized into blueprints under `Backend/api/`:

- `auth` &mdash; login, registration, and authentication-related operations
- `users` &mdash; CRUD operations for users
- `problems` &mdash; listing and retrieving Codeforces problems with estimated ratings
- `attempts` &mdash; recording user attempts and solve times
- `ratings` &mdash; adjusting and recalculating problem difficulty ratings
- `health` &mdash; simple health check endpoint (e.g. for uptime monitoring)

Refer to the docstrings and route definitions in these modules for the most up-to-date request/response formats.

## Development Notes

- Keep new endpoints grouped logically under the existing blueprints in `Backend/api/`.
- Domain logic that is not tied to Flask should live in `Backend/entities/`.
- If you introduce a database or ORM, extend `Backend/models.py` or `Backend/models/` accordingly and update configuration in `Backend/config.py`.

## Scripts

The `scripts/test_user_requests.py` script can be used as a simple manual test harness for exercising user-related endpoints (e.g. registration and login). Adjust URLs and payloads inside the script if you change API paths or ports.

## Future Work

- Add automated tests for API endpoints (e.g. with Pytest and Flask's test client).
- Document each endpoint (OpenAPI/Swagger or similar) and provide example requests.
- Add CI workflows for linting, testing, and building the Docker image.

