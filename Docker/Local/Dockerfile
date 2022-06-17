FROM python:3.9.10
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

WORKDIR /
COPY . /
WORKDIR /Requirements
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN ls -a
RUN pwd
RUN /usr/local/bin/python -m pip install -r local.txt
WORKDIR /
WORKDIR /App
