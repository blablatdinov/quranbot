FROM postgres:12.0-alpine

ENV POSTGRES_USER="qbot"
ENV POSTGRES_PASSWORD="qbot"
ENV POSTGRES_DB="qbot_db"

RUN wget https://quranbot.blablatdinov.ru/dumps/db_dump_dev.sql.tar.gz
RUN tar -xvf db_dump_dev.sql.tar.gz -C /
RUN mv /dump.sql /docker-entrypoint-initdb.d
