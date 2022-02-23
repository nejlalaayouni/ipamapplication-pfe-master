FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . /app/

RUN pip3 install mysqlclient
RUN pip3 install django-apscheduler
RUN pip3 install djangorestframework
RUN pip3 install django-rest-auth