# carrega a imagem do postgres
FROM postgres:15.2

RUN mkdir utfpr_chatbot utfpr_chatbot/DDL utfpr_chatbot/data
COPY ./DDL/* utfpr_chatbot/DDL
COPY ./data_202201/* utfpr_chatbot/data

# RUN ["/usr/local/bin/docker-entrypoint.sh", "postgres"]

# RUN psql -d utfpr_chatbot -U utfpr_chatbot  -c "\i utfpr_chatbot/DDL/CAMPUS.sql"

# RUN psql -d utfpr_chatbot -U utfpr_chatbot  -c "\copy $TBALE_NAME from '$CSV_DIR/$FILE_NAME' DELIMITER E'\t' csv"
