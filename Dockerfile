FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app.py .

# Expose port
EXPOSE 8000

# Run with Gunicorn: 4 workers, bind to all interfaces on port 8000
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "--timeout", "30", "app:app"]
