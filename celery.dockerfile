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

WORKDIR /src
