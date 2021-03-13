FROM postgres:12.0-alpine

ENV POSTGRES_USER="qbot"
ENV POSTGRES_PASSWORD="qbot"
ENV POSTGRES_DB="qbot_db"

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN wget https://quranbot.blablatdinov.ru/dumps/dev_dump.sql.gz
RUN gunzip db_dump_dev.sql.gz
RUN mv db_dump_dev.sql /docker-entrypoint-initdb.d
