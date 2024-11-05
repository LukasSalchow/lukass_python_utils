FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get install build-essential git -y
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir poetry
