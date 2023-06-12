# carrega a imagem do postgres
FROM aurelixv/postgres:latest

COPY ./database/ingestion.sh /docker-entrypoint-initdb.d/ingestion.sh
COPY ./database/data_csv /utfpr_chatbot/data
COPY ./database/DDL /utfpr_chatbot/DDL
