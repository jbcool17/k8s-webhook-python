# https://hub.docker.com/_/python
FROM python:3.9-slim

# RUN apt-get update && \
#     apt-get install --yes --no-install-recommends git wget && \
#     git --version

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

# https://stackoverflow.com/questions/54597500/printing-not-being-logged-by-kubernetes
ENTRYPOINT [ "python", "/app/webhook.py" ]
