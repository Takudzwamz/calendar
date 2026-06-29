# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY . .

# Run as a non-root user
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /usr/src/app
USER appuser

# App listens internally on 8080 (Caddy reverse-proxies 80/443 -> here)
EXPOSE 8080

# FLASK_SECRET_KEY is supplied at runtime via env_file (.env.app), never baked in
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/robots.txt', timeout=4).status==200 else 1)"

# Production WSGI server (no Flask dev server / debug mode)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "app:app"]
