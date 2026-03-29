ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0
WORKDIR /app
COPY --from=workspace pyproject.toml uv.lock ./
COPY --from=workspace nanobot/ ./nanobot/
COPY --from=workspace mcp/mcp-lms/ ./mcp/mcp-lms/
RUN --mount=type=cache,target=/root/.cache/uv uv sync
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LANG=C.UTF-8
RUN apt-get update && apt-get install -y gosu && rm -rf /var/lib/apt/lists/*
ARG APP_UID=1000 APP_GID=1000
RUN groupadd --system --gid ${APP_GID} appgroup && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home appuser
COPY --from=builder --chown=appuser:appgroup /app /app
RUN mkdir -p /app/nanobot/workspace/{cron,sessions,memory} && chown -R appuser:appgroup /app/nanobot/workspace
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
USER appuser
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:18790/health')" || exit 1
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "/app/nanobot/entrypoint.py"]
