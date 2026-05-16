# Use a slim Python image (update version as needed)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Install system dependencies (for psycopg2 and common needs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project code
COPY . .

# Collect static files (run during build or in entrypoint)
RUN mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Gunicorn port (internal only)
EXPOSE 8000

# Default command (override in compose if needed)
CMD ["gunicorn", "nowplay_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2"]
