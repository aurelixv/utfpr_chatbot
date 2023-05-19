# carrega a imagem do rasa-sdk
FROM rasa/rasa-sdk:3.5.1

# muda para usuário root
USER root

# instala curl
RUN apt update && apt install curl -y

# instala pacotes python
RUN pip install pyyaml
RUN pip install unidecode
RUN pip install psycopg2-binary

# retorna para usuário comum
USER 1001
