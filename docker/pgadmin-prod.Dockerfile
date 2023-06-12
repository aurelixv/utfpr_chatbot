# carrega a imagem do ngrok
FROM aurelixv/pgadmin:latest

COPY ./pgadmin/servers.json /pgadmin4/servers.json
COPY ./pgadmin/pgpass /root/.pgadmin
