FROM python:3.7-slim
WORKDIR /app
RUN apt-get update
RUN apt-get install libpq-dev gcc chromium chromium-driver -y
RUN apt-get install -y --no-install-recommends libc-dev
WORKDIR /app
RUN pip3 install pipenv
ADD Pipfile* /app/
RUN pipenv sync -d
ADD . /app