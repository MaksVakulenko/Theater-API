FROM python:3.12
LABEL authors="maksimvakulenkooo@gmail.com"

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y dos2unix

WORKDIR /usr/requirements

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /usr/app

COPY . .

COPY ./commands /usr/src/commands

RUN dos2unix /usr/src/commands/*.sh