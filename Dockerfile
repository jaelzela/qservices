FROM python:2-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apk add --no-cache bash
ADD . /code/
RUN python manage.py migrate