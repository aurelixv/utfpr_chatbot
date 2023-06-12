# carrega a imagem do rasa-sdk
FROM aurelixv/rasa-actions:latest

COPY ./bot/actions /app/actions
COPY ./bot/endpoints.yml /app/endpoints.yml
