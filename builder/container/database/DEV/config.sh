#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE TABLESPACE sofia_core_dev OWNER postgres LOCATION '/data';
    CREATE DATABASE sofia_core_dev OWNER postgres TABLESPACE sofia_core_dev;
EOSQL