FROM python:3.10-slim

WORKDIR /core

COPY ./core /core
COPY requirements.txt /core

RUN apt upgrade

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python /core/main.py