FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING=utf-8
ENV POETRY_VERSION=1.5

RUN apt-get update && apt-get install -y vim && apt-get upgrade -y
RUN pip install --upgrade pip "poetry==$POETRY_VERSION"

COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock

RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY . ./src
ENV PATH "$PATH:/src/scripts"

RUN useradd -m -d /src -s /bin/bash app  \
    && chown -R app:app /src/* && chmod +x /src/scripts/*

RUN mkdir -p /src/static
RUN chmod 777 -R /src/static

WORKDIR /src
USER app
