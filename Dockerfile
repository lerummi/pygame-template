FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends git build-essential curl ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy project files including pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Sync dependencies as defined in pyproject.toml and uv.lock
RUN uv sync

EXPOSE 8061

ENTRYPOINT [  ]