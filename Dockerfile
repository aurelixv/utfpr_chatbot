# carrega a imagem do ubuntu
FROM ubuntu:20.04

ENTRYPOINT []

# atualiza para o python 3.9 e instala o rasa 3.1.0
RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.9 && apt install -y python3-pip
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install rasa==3.1.0 --no-cache-dir

# define diretorio /app e copia conteudo do bot
WORKDIR /app
ENV HOME=/app
COPY /bot .
COPY start_services.sh .

# roda codigo shell para pegar porta dinamica do heroku
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh
