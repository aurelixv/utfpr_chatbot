train:
	docker run -v "$(shell pwd)/bot:/app" aurelixv/rasa_server:latest train --fixed-model-name nlu_utfpr_chatbot
run:
	docker compose up
clean:
	docker compose down && \
		docker compose build --no-cache && \
		docker compose up
build-server:
	cd rasa_server/ && \
		docker build -t aurelixv/rasa_server . && \
		docker push aurelixv/rasa_server:latest
build-actions:
	cd rasa_actions/ && \
		docker build -t aurelixv/rasa_actions . && \
		docker push aurelixv/rasa_actions:latest
build-postgres:
	cd postgres/ && \
	docker build -t aurelixv/postgres . && \
	docker push aurelixv/postgres:latest
deploy:
	heroku container:login && \
	heroku container:push web -a utfpr-chatbot
release:
	heroku container:release web -a utfpr-chatbot
ngrok:
	ngrok http 5005
clear-bot-cache:
	rm -r bot/.rasa/*
psql:
	heroku pg:psql -a utfpr-chatbot
