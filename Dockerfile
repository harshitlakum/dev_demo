
# Multi-stage: build deps, then a slim runtime
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Install system deps (none required now, but keep pip up-to-date)
RUN python -m pip install --upgrade pip

# Install Python deps first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app /app/app

# Create non-root user
RUN useradd -m appuser
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
