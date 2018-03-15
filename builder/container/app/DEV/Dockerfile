FROM debian:stretch

RUN apt-get update && apt-get install -y --allow-unauthenticated python3-django python3-pip vim nginx git && \
    cd /srv && git clone -b develop https://github.com/willcode-labs/sofia.git && \
    mkdir /srv/sofia/log && cd /srv/sofia && pip3 install --no-cache-dir -r requirements.txt && \
    rm /etc/nginx/sites-available/default && \
    ln -s /srv/sofia/builder/container/app/DEV/sofia_nginx.conf /etc/nginx/sites-enabled/

WORKDIR /srv/sofia

VOLUME ["/srv/sofia"]

CMD /etc/init.d/nginx restart && uwsgi --socket sofia.sock --module sofia.wsgi --chmod-socket=666
