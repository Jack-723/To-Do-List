# Use official Python runtime as base image
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port 8080 (Cloud Run uses this)
EXPOSE 8080

# Run the application
# Cloud Run sets PORT environment variable to 8080
CMD exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}