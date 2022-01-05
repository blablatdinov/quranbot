FROM postgres:14.1-alpine

ENV POSTGRES_USER="qbot"
ENV POSTGRES_PASSWORD="qbot"
ENV POSTGRES_DB="qbot_db"

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN wget https://quranbot.blablatdinov.ru/dumps/dev_dump.sql.gz
RUN mv dev_dump.sql.gz docker-entrypoint-initdb.d
