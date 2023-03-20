FROM python:3.10.5
WORKDIR /app
RUN apt update
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
