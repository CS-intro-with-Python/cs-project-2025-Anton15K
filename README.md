[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DESIFpxz)
# CS_2025_project

## Description

A full-stack web application for tracking Codeforces problem-solving performance with intelligent rating estimation. The system analyzes solver data from Codeforces contests to estimate problem difficulty and calculate user performance ratings.

### Key Features

- **User Authentication**: Registration, login, and session management
- **Problem Management**: Add Codeforces problems with automatic rating estimation
- **Timer-based Attempts**: Track solve times with start/stop timer functionality
- **Codeforces Integration**: Verify solutions and fetch solver data from CF API
- **Performance Analytics**: Calculate performance ratings and rating deltas based on solve times
- **Bayesian Rating Updates**: Problem ratings improve over time based on local solve data

## Tech Stack

- **Backend**: Flask, Jinja2
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Styling**: Tailwind CSS
- **External API**: Codeforces API

## Project Structure

```text
Backend/
    app.py                    # Application factory / entry point
    config.py                 # Configuration settings
    extensions.py             # Flask extensions (SQLAlchemy, etc.)
    views.py                  # Frontend page routes and logic
    models.py                 # Database model exports
    api/                      # REST API blueprints
        auth.py               # Authentication endpoints
        users.py              # User management endpoints
        problems.py           # Problem CRUD + estimation
        attempts.py           # Attempt start/complete endpoints
        ratings.py            # Rating calculation endpoints
        codeforces.py         # CF API integration endpoints
        health.py             # Health check endpoint
    entities/                 # SQLAlchemy ORM models
        user.py               # User model (rating, cf_handle)
        problem.py            # Problem model (estimated_rating)
        attempt.py            # Attempt model (duration, performance)
        rating_adjustment.py  # Rating adjustment records
    tools/                    # Business logic utilities
        cf_api.py             # Codeforces API client
        advanced_rating_logic.py  # Rating algorithms
    templates/                # Jinja2 HTML templates
        base.html             # Base layout with navbar
        index.html            # Home page
        auth/                 # Login/register pages
        problems/             # Problem list/detail pages
        attempts/             # Attempt history page
        profile/              # User profile page
        codeforces/           # CF lookup tools
    static/                   # CSS/JS assets

db/
    init.sql                  # Database schema initialization

scripts/
    test_user_requests.py     # API smoke tests

.github/workflows/
    backend-smoke.yml         # CI pipeline for testing
```

## Local Setup

### Prerequisites

- Python 3.10+
- Docker and Docker Compose (recommended)
- Or: `pip`, `venv`, and PostgreSQL

### Running with Docker Compose (Recommended)

```bash
# Clone and enter directory
git clone <your-repo-url> && cd cs-project-2025-Anton15K

# Start all services (Postgres + Backend)
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down

# Stop and remove all data
docker compose down -v
```

The app will be available at `http://localhost:5001`.

### Running without Docker

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL and configure DATABASE_URL
export DATABASE_URL=postgresql://user:pass@localhost/dbname

# Run the Flask app
cd Backend
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --port 5001
```

## API Overview

All API endpoints are prefixed with `/api/v1/`.

| Blueprint    | Description                                          |
|--------------|------------------------------------------------------|
| `auth`       | Login, registration, logout                          |
| `users`      | User CRUD, current user info                         |
| `problems`   | Problem list, create, get, estimate from CF          |
| `attempts`   | Start/complete attempts, history                     |
| `ratings`    | Calculate performance, delta, adjust ratings         |
| `codeforces` | User lookup, problem analysis, submission check      |
| `health`     | Health check (`/api/v1/health`)                      |

### Frontend Pages

| Route           | Description                         |
|-----------------|-------------------------------------|
| `/`             | Home page with stats                |
| `/login`        | Login form                          |
| `/register`     | Registration form                   |
| `/problems`     | Problem list + add form             |
| `/problems/<id>`| Problem detail                      |
| `/attempts`     | Active attempt timer + history      |
| `/profile`      | User profile with rating            |
| `/codeforces`   | CF user/problem lookup tools        |

## Rating System

### Problem Difficulty Estimation

When a problem is added with `contest_id` and `problem_index`, the system:
1. Fetches all solvers from Codeforces contest standings
2. Gets each solver's rating at the time of the contest
3. Calculates estimated difficulty as the **mean solver rating**

### Performance Rating Calculation

When a user completes a problem, their performance rating is calculated using **regression analysis**:
- Model: `log(net_time) = a + b * rating`
- The user's time is mapped to an implied rating based on how fast they solved relative to other solvers

### Rating Delta (Elo-style)

```
delta = k_factor * (actual_score - expected_score) * scale_factor
```

- **Expected score**: Based on user rating vs problem rating (Elo formula)
- **Actual score**: Based on time percentile (faster = higher)
- **Scale factor**: Amplified if performance rating differs significantly from user rating

### Bayesian Problem Rating Updates

After each solve, the problem's estimated rating is updated:
- Uses a **Bayesian posterior** combining CF data (prior) with local performance data
- Higher-rated solvers contribute more weight
- Confidence increases with more attempts

## Submission Verification

The timer system includes Codeforces submission verification:

1. **On Start**: Checks if user already solved the problem on CF → blocks if yes
2. **On Complete**: Verifies that user submitted a correct solution *after* the timer started
3. **Checks last 50 submissions** to avoid missing older submissions

## Testing

### Run API Smoke Tests

```bash
# With Docker running
python3 scripts/test_user_requests.py
```

### GitHub Actions CI

The `backend-smoke.yml` workflow runs on every push:
1. Builds Docker containers
2. Waits for health check
3. Runs all API smoke tests

## Success Criteria

### Authentication & User Management
- [ ] Users can register with username, email, password, and optional CF handle
- [ ] Users can log in and maintain session across pages

### Problem Management
- [ ] Problems can be added with Codeforces contest ID and problem index
- [ ] System automatically estimates problem difficulty from CF solver data
- [ ] Problem list shows all problems with their estimated ratings

### Timer & Attempt Tracking
- [ ] Users can start a timed attempt for any problem
- [ ] Attempt history shows duration and performance metrics

### Codeforces Verification
- [ ] System verifies submissions via CF API on attempt completion
- [ ] User receives feedback on verification status

### Rating System
- [ ] Performance rating calculated based on solve time vs other solvers
- [ ] Rating delta applied to user rating after each solved attempt


