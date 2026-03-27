FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize a git repo so the script's git operations don't fail
RUN git config --global user.email "container@test" && \
    git config --global user.name "test" && \
    git init && git add -A && git commit -m "init"

ENTRYPOINT ["./entrypoint.sh"]
