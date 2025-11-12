
FROM python:3.12-slim



# Create app directory
WORKDIR /app

RUN pip install --upgrade pip

# Install Python dependencies (no requirements.txt yet)
RUN pip install \
    Flask \
    Flask-CORS \
    Flask-Login \
    requests

# Copy backend source
COPY Backend ./Backend

# Expose the Flask port
EXPOSE 5001

# Run the app using the factory pattern entrypoint
CMD ["flask", "--app", "Backend.app:create_app", "run", "--host=0.0.0.0", "--port=5001"]
