FROM python:3.8.1-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP /usr/src/app/app.py
ENV APP_SETTINGS config.DevelopmentConfig
ENV DATABASE_URL postgresql://wimp_user:wimp_code_vs_covid1920_pagio@db/wimp
ENV FLASK_DEBUG False

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt


COPY . /usr/src/app/

RUN chmod u+x ./wait-for-it.sh

ENTRYPOINT ./wait-for-it.sh db:5432 -- python manage.py db upgrade && gunicorn -w 4 --bind 0.0.0.0:5000 app:app
