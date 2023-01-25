FROM python:3.10-slim-buster
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY . /app
