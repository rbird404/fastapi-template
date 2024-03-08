FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING=utf-8

RUN apt-get update && apt-get install -y vim && apt-get upgrade -y

COPY ./requirements/requirements.txt /requirements.txt

COPY . ./src

RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

ENV PATH "$PATH:/src/scripts"

RUN useradd -m -d /src -s /bin/bash app  \
    && chown -R app:app /src/* && chmod +x /src/scripts/*

RUN mkdir -p /src/static
RUN chmod 777 -R /src/static

WORKDIR /src
USER app
