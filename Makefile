.PHONY: train up stop down clean build ngrok clear-bot-cache

train:
	docker run --name rasa-train -v "$(shell pwd)/bot:/app" aurelixv/rasa-server:latest train --fixed-model-name nlu_utfpr_chatbot && \
		docker rm rasa-train
up:
	docker compose up -d
stop:
	docker compose stop
down:
	docker compose down
clean:
	docker compose down && \
		docker compose up -d
build:
	docker compose build --no-cache && \
		docker compose push
ngrok:
	ngrok http 5005 --config ./ngrok/ngrok.yml
clear-bot-cache:
	rm -r bot/.rasa/*
