FROM postgres:latest

COPY init.sh /docker-entrypoint-initdb.d/
RUN chmod 777 /docker-entrypoint-initdb.d/init.sh

# CMD [ "/docker-entrypoint-initdb.d/init.sh" ]
