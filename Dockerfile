# carrega a imagem do ubuntu
FROM aurelixv/ubuntu:latest

ENTRYPOINT []

# define diretorio /app e copia conteudo do bot
WORKDIR /app
ENV HOME=/app
COPY /bot .
COPY start_services.sh .

# roda codigo shell para pegar porta dinamica do heroku
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh
