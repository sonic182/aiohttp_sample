FROM python:3.5

WORKDIR /usr/src/app
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /usr/src/app
