FROM postgres:12.0-alpine

ENV POSTGRES_USER="qbot"
ENV POSTGRES_PASSWORD="qbot"
ENV POSTGRES_DB="qbot_db"

RUN wget https://quranbot.blablatdinov.ru/dumps/db_dump_dev.sql.tar.gz
RUN tar -xvf db_dump_dev.sql.tar.gz -C /
# RUN psql -U qbot qbot_db < some_file.sql
# docker build -t qbot_db ./
# docker run -d --name qbot_db qbot_db
# psql -U qbot -d qbot_db < some_file.sql
# docker exec -ti qbot_db bash
# docker stop qbot && docker rm qbot_db && docker build -t qbot_db ./
