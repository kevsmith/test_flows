FROM --platform=linux/amd64 python:3.8

RUN apt-get update && apt-get upgrade -y && apt-get -y install inetutils-tools

RUN pip install --upgrade pip && pip install nats-py

COPY hook.py /hook.py

CMD python /hook.py