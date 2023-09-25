.PHONY: train up stop down clean build push ngrok update-webhook clear-bot-cache ignore-credentials

train:
	docker run --name rasa-train -v "$(shell pwd)/bot:/app" aurelixv/rasa-server:latest train --fixed-model-name nlu_utfpr_chatbot && \
		docker rm rasa-train
up:
	docker compose up -d
stop:
	docker compose stop
down:
	docker compose down -v
clean:
	docker compose down && \
		docker compose up -d
build:
	docker compose build --no-cache
push:
	docker compose push
ngrok:
	nohup ngrok http 5005 --config ./ngrok/ngrok.yml --log=stdout > ngrok/ngrok.log &
update-webhook:
	python ngrok/update_webhook_url.py
clear-bot-cache:
	rm -r bot/.rasa/*
ignore-credentials:
	git update-index --skip-worktree ngrok/ngrok.yml
	git update-index --skip-worktree bot/credentials.yml
