
FROM python:3.12-slim

# Create app directory
WORKDIR /app

RUN pip install --upgrade pip

# Copy dependency specification and install Python dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY Backend ./Backend

# Expose the Flask port
EXPOSE 5001

# Run the app using the factory pattern entrypoint
CMD ["flask", "--app", "Backend.app:create_app", "run", "--host=0.0.0.0", "--port=5001"]
