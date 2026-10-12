# Multi-stage / optimized slim production container for FitTrack
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered streaming logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/app/data/fittrack.db \
    PORT=5000 \
    HOST=0.0.0.0

# Set container working directory
WORKDIR /app

# Install curl for container health check probes and system security updates
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root system group and user
RUN groupadd -g 1001 fittrack && \
    useradd -u 1001 -g fittrack -m -s /bin/bash fittrack

# Copy requirements and install dependencies without cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY config.py app.py /app/
COPY database/ /app/database/
COPY routes/ /app/routes/
COPY services/ /app/services/
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY scripts/ /app/scripts/

# Create persistent data directory and grant non-root permissions
RUN mkdir -p /app/data && \
    chown -R fittrack:fittrack /app

# Switch to non-root user
USER fittrack

# Declare persistent volume mount point for SQLite database
VOLUME ["/app/data"]

# Expose production port
EXPOSE 5000

# Container healthcheck querying the /api/health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Production WSGI server execution
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
