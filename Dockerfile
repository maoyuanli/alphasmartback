FROM python:3.7.5-stretch
MAINTAINER Maotion FinTech Ltd.

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader vader_lexicon
RUN python -m nltk.downloader punkt


COPY . /code/

