FROM python:3.11.1-slim

## ENVS variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

## System dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential
RUN rm -rf /var/lib/apt/lists/*

## Project dependencies
COPY ./Envs/Dev/requirements.txt /tmp/Requirements/Dev/
COPY ./Envs/default_requirements.txt /tmp/Requirements/
COPY ./Envs/format_requirements.txt /tmp/Requirements/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/Requirements/Dev/requirements.txt
RUN rm -r -f /tmp/Requirements

## Project files
RUN mkdir -p /App/
COPY ./Project /App/Project
COPY ./manage.py /App/
COPY ./Apps /App/Apps
COPY ./Envs/__init__.py /App/Envs/__init__.py
COPY ./Envs/Dev/__init__.py /App/Envs/Dev/__init__.py
COPY ./Envs/Dev/django_settings.py /App/Envs/Dev/django_settings.py
WORKDIR /App

## Image configuration
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
