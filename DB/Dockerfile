FROM postgres:latest
USER postgres
RUN docker-entrypoint.sh postgres
RUN psql --username=postgres --command='CREATE USER mlcuser WITH PASSWORD ${password}'
RUN createdb --username=postgres --owner=mlcuser mlcdb
RUN psql --username=postgres --dbname=cmsdb --command='ALTER SCHEMA public OWNER TO mlcuser'
RUN service postgresql stop
