# Minimal Dockerfile for the Flask backend scaffold
# Builds a small image and runs the app with the Flask CLI

FROM python:3.12-slim

# Environment hygiene and production defaults


# Create app directory
WORKDIR /app

# Upgrade pip first for reliability
RUN pip install --upgrade pip

# Install Python dependencies (no requirements.txt yet by design)
RUN pip install \
    Flask \
    Flask-RESTX \
    Flask-CORS \
    Flask-Login \
    Flask-SQLAlchemy \
    requests

# Copy backend source
COPY Backend ./Backend

# Expose the Flask port
EXPOSE 5001

# Run the app using the factory pattern entrypoint
# Swagger UI will be available at http://localhost:5001/api/v1/docs
CMD ["flask", "--app", "Backend.app:create_app", "run", "--host=0.0.0.0", "--port=5001"]
