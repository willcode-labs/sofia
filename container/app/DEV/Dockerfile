FROM debian:latest

WORKDIR /srv

RUN apt-get update && apt-get install -y python3-django python3-pip vim nginx \
    python3-dev libpq-dev git

VOLUME ["/srv"]

RUN git clone -b develop https://github.com/willcode-labs/sofia.git

WORKDIR /srv/sofia

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 makemigrations api --check
RUN python3 migrate api
