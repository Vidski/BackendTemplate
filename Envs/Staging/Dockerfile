FROM python:3.11.1-slim
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
COPY ./Envs/Production/requirements.txt /tmp/Requirements/Production/
COPY ./Envs/default_requirements.txt /tmp/Requirements/
COPY ./Envs/format_requirements.txt /tmp/Requirements/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/Requirements/Production/requirements.txt
RUN rm -r -f /tmp/Requirements

## Project files
RUN mkdir -p /App/
COPY ./Apps /App/Apps
COPY ./Envs/__init__.py /App/Envs/__init__.py
COPY ./Envs/Production/__init__.py /App/Envs/Production/__init__.py
COPY ./Envs/Production/django_settings.py /App/Envs/Production/django_settings.py
COPY ./Envs/default_django_settings.py /App/Envs/default_django_settings.py
COPY ./Project /App/Project
COPY ./manage.py /App/
WORKDIR /App

## Image configuration
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
