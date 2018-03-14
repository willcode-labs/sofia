# https://hub.docker.com/_/postgres/
FROM postgres:10.3

ADD config.sh /docker-entrypoint-initdb.d/
RUN mkdir /data && chmod -R 777 /data && chown postgres:postgres /data
RUN localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8
ENV LANG pt_BR.utf8
USER postgres
RUN /usr/lib/postgresql/10/bin/initdb
EXPOSE 5432
