FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . /app

# Expose port
EXPOSE 5000

# Use Gunicorn to serve the app via WSGI
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5000", "--workers", "2"]
