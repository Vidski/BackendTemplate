FROM python:3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ARG ENV
WORKDIR /
COPY . /
RUN pip3 install --no-cache-dir -r ./Requirements/local.txt
WORKDIR /App
