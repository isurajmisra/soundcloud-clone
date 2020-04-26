#!/bin/bash
export PGUSER=postgres
psql <<- EOSQL
    CREATE USER postgres;
    CREATE DATABASE soundcloud;
    GRANT ALL PRIVILEGES ON DATABASE soundcloud TO postgres;
EOSQL
