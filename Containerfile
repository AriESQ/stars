FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

# Initialize a git repo so the script's git operations don't fail
RUN git config --global user.email "container@test" && \
    git config --global user.name "test" && \
    git init && git add -A && git commit -m "init"

ENTRYPOINT ["./entrypoint.sh"]
