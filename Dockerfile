FROM python:3.7-slim
MAINTAINER tools@digital.trade.gov.uk
RUN apt-get update
RUN apt-get install gcc -y
WORKDIR /app
ADD requirements*.txt /app/
RUN pip install -r requirements.txt

# RUN apt-get -y install curl
# RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
# RUN apt-get -y install nodejs
# ADD package*.json /app/
# RUN npm install
# ADD . /app