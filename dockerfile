# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.3
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

# Assurez-vous que le répertoire existe et changez les permissions avant de passer à l'utilisateur appuser
RUN mkdir -p /app/new_data && chown -R appuser:appuser /app/new_data

USER appuser

COPY . .

EXPOSE 8000

ENV POPULATE_DB=false

CMD ["python3", "main.py"]