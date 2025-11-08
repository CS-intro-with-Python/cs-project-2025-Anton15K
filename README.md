[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

## Description

This project is a full-stack web application designed to estimate the difficulty rating of Codeforces problems based on the ratings of users who solved them.

Each Codeforces problem is solved by a number of users with varying ratings. By analyzing these solver ratings, the system can estimate a possible difficulty rating for each problem.

Users can check a problem’s estimated rating, attempt the problem using a timer, and then adjust the difficulty rating based on their personal performance.  
The application provides a personalized and adaptive difficulty estimation based on user statistics, solve time, and internal rating.

The backend is implemented with Flask and provides a RESTful API.  
The frontend is built with Vue.js and communicates with the Flask API using Axios.  
All components are containerized with Docker, and the project includes continuous integration (CI) and continuous deployment (CD) via GitHub Actions and Railway.app.

## Setup

The application can be run locally or through Docker.

## Project Structure

```text
backend/                # Flask application source and tests
frontend/               # Vue 3 single-page application
instruct/               # Technical docs (e.g., implementation guide)
infrastructure/         # Deployment and ops assets
docker-compose.yml      # Local development stack definition
```

### Local Setup

```bash
# Clone repository
git clone <your-repo-url> && cd cs-project-2025-Anton15K

# Backend setup
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
flask --app app:create_app() run --port=5001

# Frontend setup
cd ../frontend
npm install
npm run dev
```

### Docker Setup

```bash
docker-compose up --build
```

### CI/CD Workflows

GitHub Actions definitions live in `.github/workflows/`:

- `backend-ci.yml` &mdash; installs backend dependencies, runs Ruff/Black, and executes Pytest with coverage export.
- `frontend-ci.yml` &mdash; installs frontend dependencies, runs ESLint/Vitest, and builds the Vue app.
- `deploy.yml` &mdash; builds Docker images and deploys to Railway on pushes to `main`. Configure the secrets `RAILWAY_TOKEN`, `RAILWAY_PROJECT_ID`, optional `RAILWAY_ENVIRONMENT`, and optional `RAILWAY_DEPLOY_COMMAND` before enabling the job.

### Additional Documentation

- Detailed step-by-step implementation guidance lives in `instruct/IMPLEMENTATION_GUIDE.md`. Keep it updated as architecture decisions evolve.

The `docker-compose.yml` defines the following services:
- Flask API
- Vue frontend
- Database (PostgreSQL or MongoDB)

## Requirements

The project uses the following technologies, tools, and languages:

| Layer | Tools / Libraries |
|-------|--------------------|
| Backend | Flask, Flask-SQLAlchemy, Flask-Login, Flask-CORS, Flask-RESTX, Pytest |
| Frontend | Vue.js 3, Vue Router, Axios, Tailwind CSS or Bootstrap |
| Database | PostgreSQL (via SQLAlchemy ORM) or MongoDB |
| Authentication | Flask-Login |
| Statistical Analysis | NumPy, Pandas, SciPy |
| API Documentation | Swagger (via Flask-RESTX) |
| CI/CD | GitHub Actions, Railway.app |
| Containerization | Docker, Docker Compose |

The backend handles data processing, authentication, and API endpoints.  
The frontend serves as a browser-based interface built with Vue.js, interacting with the Flask REST API.  
The system uses a RESTful architecture for client-server communication.

## Features

* User authentication with registration, login, and logout
* Difficulty rating estimation for Codeforces problems
* Timer feature for tracking problem-solving duration
* Adaptive difficulty adjustment based on user performance
* Optional user feedback and review system
* RESTful API documented using Swagger
* Vue-based single-page frontend application
* Responsive and modular user interface
* Automated CI/CD integration for testing and deployment

## Git

- `main`: Stable production-ready branch  
- `dev`: Active development branch  
- `feature/*`: Feature-specific branches (e.g., `feature/login`)

## Success Criteria

* REST API is functional, versioned, and documented with Swagger
* Application runs in Docker containers with working backend, frontend, and database
* Vue frontend interacts successfully with Flask backend
* CI pipeline builds, tests, and validates all components automatically
* Continuous deployment from the `main` branch is configured and functional
* Authentication and authorization features work as expected
* Rating estimation and adjustment logic produce reasonable results
* The README provides complete setup, testing, and deployment instructions
