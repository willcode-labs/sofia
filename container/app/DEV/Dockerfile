FROM debian:stretch

RUN apt-get update && apt-get install -y python3-django python3-pip vim nginx git && \
    cd /srv && git clone -b develop https://github.com/willcode-labs/sofia.git && \
    cd /srv/sofia && pip3 install --no-cache-dir -r requirements.txt && \
    ln -s /srv/sofia/container/app/DEV/sofia_nginx.conf /etc/nginx/sites-enabled/

WORKDIR /srv/sofia

VOLUME ["/srv/sofia"]
