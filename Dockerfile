FROM python:alpine
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/
ENV UV_SYSTEM_PYTHON=1
ENV UV_NO_SYNC=True

WORKDIR /app/
COPY pyproject.toml .
RUN UV_NO_SYNC=False uv sync --no-dev

COPY app.py README.md ./
COPY lookup/ lookup/
ENTRYPOINT [ "uv", "run", "litestar", "run" ]
#ENTRYPOINT [ "/bin/sh" ]
ENV LITESTAR_PORT=8000
ENV LITESTAR_HOST=0.0.0.0
EXPOSE 8000
