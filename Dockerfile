# https://hub.docker.com/_/python
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENTRYPOINT [ "python", "/app/webhook.py" ]
