.PHONY: train up stop down clean build ngrok update-webhook clear-bot-cache

train:
	docker run --name rasa-train -v "$(shell pwd)/bot:/app" aurelixv/rasa-server:latest train --fixed-model-name nlu_utfpr_chatbot && \
		docker rm rasa-train
up:
	docker compose -f docker-compose-dev.yml up -d
stop:
	docker compose -f docker-compose-dev.yml stop
down:
	docker compose down -v
clean:
	docker compose down -v && \
		docker compose -f docker-compose-dev.yml up -d
build:
	docker compose -f docker-compose-prod.yml build --no-cache
push:
	docker compose -f docker-compose-prod.yml push
ngrok:
	nohup ngrok http 5005 --config ./ngrok/ngrok.yml --log=stdout > ngrok/ngrok.log &
update-webhook:
	python ngrok/update_webhook_url.py
clear-bot-cache:
	rm -r bot/.rasa/*
