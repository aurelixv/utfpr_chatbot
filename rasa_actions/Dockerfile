# carrega a imagem do rasa-sdk
FROM rasa/rasa-sdk:3.5.1

# muda para usuário root
USER root

# instala pacotes python
RUN pip install pyyaml
RUN pip install unidecode
RUN pip install psycopg2-binary

# copia arquivo actions
# COPY ./actions.py actions/actions.py

# retorna para usuário comum
USER 1001
