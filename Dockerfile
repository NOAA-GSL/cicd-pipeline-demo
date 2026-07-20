# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and configuration
COPY main.py .
COPY pyproject.toml .
COPY static/ ./static/
COPY tests/ ./tests/

# Make port 8112 available
EXPOSE 8112

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8112"]
