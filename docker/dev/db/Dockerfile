FROM postgres:12.0-alpine

ENV POSTGRES_USER="qbot"
ENV POSTGRES_PASSWORD="qbot"
ENV POSTGRES_DB="qbot_db"

ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
# RUN wget https://quranbot.blablatdinov.ru/dumps/db_dump_dev.sql.tar.gz
# RUN tar -xvf db_dump_dev.sql.tar.gz -C /
# RUN mv home/www/code/quranbot/dumps/dump.sql /docker-entrypoint-initdb.d
