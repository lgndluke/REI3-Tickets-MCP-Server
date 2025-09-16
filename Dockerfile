FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
LABEL authors="lukas.jeckle"

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Set uv link mode
ENV UV_LINK_MODE=copy

# Set uv tool directory
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Add the rest of the project source code and install it.
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Place executables in the environment
ENV PATH='/app/.venv/bin:$PATH'

# Reset entrypoint, don't invoke uv.
ENTRYPOINT []

# RUN the application.
CMD ["python", "./rei3_tickets_mcp_server.py"]
