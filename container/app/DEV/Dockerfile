FROM debian:stretch

RUN apt-get update && apt-get install -y python3-django python3-pip vim nginx git
RUN cd /srv && git clone -b develop https://github.com/willcode-labs/sofia.git
RUN cd /srv/sofia && pip3 install --no-cache-dir -r requirements.txt

WORKDIR /srv/sofia

VOLUME ["/srv/sofia"]
