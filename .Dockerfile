# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.11-slim
FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MPLBACKEND=Agg

WORKDIR /app

# System deps (keep minimal; wheels should satisfy most builds)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default runtime env hints (overridable at run time)
ENV PLOTS_DIR=/app/data/plots \
    STATIC_DIR=/app/static

# Create required directories
RUN mkdir -p "$PLOTS_DIR" "$STATIC_DIR"

# Run the Telegram bot
CMD ["python", "-m", "app.bot"]


