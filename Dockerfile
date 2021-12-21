from python:latest

RUN apt-get update \
    && apt-get upgrade -y

RUN python -m pip install black

