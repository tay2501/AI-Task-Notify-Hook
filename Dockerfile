# Multi-stage build for AI Task Notify Hook
FROM python:3.12-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies and build
RUN uv sync --frozen --no-dev
RUN uv run poly build

# Production image
FROM python:3.12-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libdbus-1-3 \
    libnotify4 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy built application
COPY --from=builder /app/projects/*/dist/*.whl /tmp/wheels/

# Install the application
RUN pip install /tmp/wheels/*.whl && rm -rf /tmp/wheels

# Switch to non-root user
USER app

# Default command
CMD ["notify-tool", "--help"]

# Server variant
FROM production as server
CMD ["notify-server"]

# CLI variant
FROM production as cli
CMD ["notify", "--help"]