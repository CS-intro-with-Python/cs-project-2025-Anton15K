# Implementation Guide

This guide details the steps required to build the Codeforces difficulty estimation platform described in the project README. It is organized into phases that can be executed sequentially or in parallel where noted.

---

## 1. Project Initialization

1. **Create repository structure**
   - Root directories: `backend/`, `frontend/`, `infrastructure/`, `docs/`, `scripts/`.
   - Shared config: `.editorconfig`, `.gitignore`, `README.md` updates.
2. **Choose package managers**
   - Backend: Python 3.11 runtime managed with `pip` + `pip-tools` (or `poetry`).
   - Frontend: Node.js 20.x with `pnpm` or `npm` (use the same across team).
3. **Set up virtual environments**
   - Python: `python -m venv .venv` within `backend/`.
   - Node: ensure `node_modules/` is ignored, commit `package-lock.json`/`pnpm-lock.yaml`.

## 2. Backend (Flask) Foundation

1. **Scaffold Flask app**
   - Files: `backend/app/__init__.py`, `backend/app/config.py`, `backend/wsgi.py`.
   - Use application factory pattern, enable CORS, register Blueprints (`auth`, `problems`, `users`).
2. **Configuration management**
   - Load settings from environment via `python-dotenv` (e.g., `.env`, `.env.example`).
   - Define config classes (Development, Production, Testing) within `config.py`.
3. **Database setup**
   - Choose PostgreSQL + SQLAlchemy. Initialize `db = SQLAlchemy()`.
   - Create Alembic migrations (`alembic.ini`, `migrations/`).
4. **User authentication**
   - Models: `User` (id, username, email, password_hash, cf_handle, rating, created_at).
   - Integrate `Flask-Login`, `Flask-Bcrypt`. Implement registration, login, logout endpoints.
5. **Problem and rating models**
   - Models: `Problem` (id, codeforces_id, title, tags, url), `ProblemStat`/`Solve` linking user attempts.
   - Store historical solver rating distributions for algorithm input.
6. **Difficulty estimation service**
   - Create service module using NumPy/Pandas/SciPy to calculate estimated rating from solver ratings.
   - Outline algorithm: cleaning outliers, computing weighted mean/median, storing results.
7. **REST API structure**
   - Use `Flask-RESTX` for namespacing and Swagger docs at `/api/docs`.
   - Namespaces: `/auth`, `/problems`, `/analytics`, `/users`.
   - Implement CRUD endpoints and validation (Marshmallow schemas or RESTX models).
8. **Timer & attempt tracking**
   - Endpoint to start/stop attempts, capture duration, success status, user feedback.
   - POST attempt results triggers difficulty adjustment logic.
9. **Testing**
   - Configure Pytest: fixtures for app, client, database. Include coverage config.
   - Write unit tests for models, services, API endpoints (auth, problems, rating).

## 3. Frontend (Vue 3) Foundation

1. **Scaffold Vue project**
   - Use Vite + Vue 3 in `frontend/`. Include TypeScript, Pinia for state, Vue Router.
2. **Project structure**
   - `src/`: `components/`, `views/`, `store/`, `services/`, `router/`, `styles/`.
   - Global styles configured for Tailwind CSS (or Bootstrap Vue if preferred).
3. **Routing**
   - Pages: `Home`, `ProblemExplorer`, `Attempt`, `Profile`, `Login`, `Register`.
   - Guarded routes for authenticated pages.
4. **State management**
   - Pinia store modules: `authStore`, `problemStore`, `attemptStore`, `uiStore`.
   - Persist auth tokens using `localStorage` with refresh logic.
5. **API client**
   - Axios instance with base URL (`/api`), interceptors for auth tokens, error handling.
6. **UI components**
   - Shared components: `Navbar`, `Footer`, `ProblemCard`, `DifficultyBadge`, `Timer`, `FeedbackModal`.
   - Responsive layout with Tailwind utility classes.
7. **Problem explorer workflow**
   - Fetch list of problems with estimated rating and tags.
   - Filter/search UI with rating range slider, tags, solved status.
8. **Attempt timer view**
   - Timer component with start/pause/stop, logs time to store, sends result to backend.
9. **Analytics & profile**
   - Display user stats (recent attempts, rating trend) using chart library (Chart.js or ECharts).
10. **Testing**
    - Configure Vitest + Vue Test Utils for unit tests.
    - Add E2E tests with Playwright or Cypress (later phase).

## 4. Integration Between Frontend and Backend

1. **Auth flow**
   - On login/register, store JWT or session cookie. Backend issues tokens; implement refresh endpoint.
   - Guard API routes requiring auth with decorator/middleware.
2. **Problem data synchronization**
   - Backend exposes `/api/problems` with pagination, filters.
   - Frontend caches results, handles loading/error states.
3. **Attempt submission**
   - POST `/api/attempts` with duration, success flag, optional notes.
   - Backend recalculates personalized difficulty and returns updated values.
4. **User feedback loop**
   - Optional: allow manual difficulty adjustment; backend blends user feedback with statistical model.
5. **Real-time or polling**
   - Consider WebSocket or SSE channel for live updates (optional stretch goal).

## 5. Data Ingestion from Codeforces

1. **External API integration**
   - Create `scripts/fetch_codeforces.py` to pull problem + submission data via Codeforces API.
   - Store results in staging tables (`Problem`, `SolverRatingSnapshot`).
2. **Scheduler**
   - Use Celery + Redis or simple cron (e.g., `apscheduler`) to refresh data daily.
3. **Data cleaning & caching**
   - Normalize ratings, remove duplicates, handle API rate limits.
   - Cache responses to reduce API load (Redis layer optional initially).

## 6. Docker & Environment

1. **Dockerfiles**
   - Backend: multi-stage build (builder + runtime), expose port 5001.
   - Frontend: build stage (Vite), nginx runtime serving static files.
2. **Docker Compose**
   - Services: `backend`, `frontend`, `db` (Postgres), optional `redis`, `worker`.
   - Configure networks, volumes, healthchecks.
3. **Environment configuration**
   - Provide `.env.docker` for compose, `.env.example` for local development.
   - Use secrets for production deployments.

## 7. CI/CD Pipeline

1. **GitHub Actions workflow**
   - Trigger on push/PR to `dev`, `main`.
   - Jobs: lint/test backend, lint/test frontend, build Docker images, run integration tests.
2. **Deployment pipeline**
   - For Railway.app: define `railway.json` or use CLI deploy step.
   - Auto-deploy from `main` after successful CI.
3. **Quality gates**
   - Enforce code formatting (Black, isort, Ruff; Prettier/ESLint). Fail build on lint/test errors.
   - Upload coverage reports to Codecov (optional).

## 8. Documentation & Developer Experience

1. **API documentation**
   - Maintain Swagger UI via `Flask-RESTX`. Keep models synced with responses.
2. **Developer docs**
   - Expand README with setup, running, testing, deployment instructions.
   - Add `docs/architecture.md` describing system components, data flow diagrams.
3. **Scripts**
   - Provide Makefile or `scripts/` for common tasks (format, lint, test, run).
4. **Monitoring & Logging**
   - Standardize logging with `structlog` or Python `logging` + JSON output.
   - Integrate Sentry or similar for error tracking in production (optional).

## 9. Stretch Goals & Enhancements

- Personalized recommendation engine for next problems based on user performance.
- Leaderboards and social features.
- Mobile-friendly PWA optimizations (offline caching, push notifications).
- AB testing for difficulty adjustment strategies.

---

## Implementation Checklist Summary

- [ ] Backend scaffolding with authentication, problem models, rating service
- [ ] Frontend Vite/Vue setup with routing, state, UI components
- [ ] REST API integration with Axios client
- [ ] Data ingestion scripts for Codeforces API
- [ ] Docker Compose orchestration for dev/prod
- [ ] CI/CD workflow with automated tests and deployments
- [ ] Documentation, scripts, and quality tooling

Use this guide as a living document—update steps as design decisions evolve and implementation details become concrete.
