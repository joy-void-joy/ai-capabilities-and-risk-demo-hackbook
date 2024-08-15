# Adapted from https://github.com/gianfa/poetry/blob/docs/docker-best-practices/docker-examples/minimum-poetry/Dockerfile, MIT License
FROM python:3.12-slim
ARG POETRY_VERSION=1.8

RUN pip install "poetry==${POETRY_VERSION}"

WORKDIR /app

COPY pyproject.toml .
RUN poetry install
