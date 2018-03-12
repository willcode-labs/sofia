FROM postgres:10.3

RUN mkdir /data && chmod -R 777 /data && chown postgres /data
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE TABLESPACE sofia_core_dev OWNER postgres LOCATION '/data';" && \
    psql --command "CREATE DATABASE sofia_core_dev OWNER postgres TABLESPACE sofia_core_dev;"

RUN echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/10.3/main/pg_hba.conf && \
    echo "listen_addresses='*'" >> /etc/postgresql/10.3/main/postgresql.conf

EXPOSE 5432

CMD [
    "/usr/lib/postgresql/10.3/bin/postgres",
    "-D",
    "/var/lib/postgresql/10.3/main",
    "-c",
    "config_file=/etc/postgresql/10.3/main/postgresql.conf"]