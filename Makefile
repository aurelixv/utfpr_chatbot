train:
	docker run -v "$(shell pwd)/bot:/app" aurelixv/rasa_server:latest train --fixed-model-name nlu_utfpr_chatbot
run:
	docker compose up
clean:
	docker compose down && \
		docker compose build --no-cache && \
		docker compose up
build-server:
	cd docker/ && \
		docker build -f rasa_server.Dockerfile -t aurelixv/rasa_server . && \
		docker push aurelixv/rasa_server:latest
build-actions:
	cd docker/ && \
		docker build -f rasa_actions.Dockerfile -t aurelixv/rasa_actions . && \
		docker push aurelixv/rasa_actions:latest
build-postgres:
	cd docker/ && \
		docker build -f postgres.Dockerfile -t aurelixv/postgres . && \
		docker push aurelixv/postgres:latest
build-ngrok:
	cd docker/ && \
		docker build -f ngrok.Dockerfile -t aurelixv/ngrok . && \
		docker push aurelixv/ngrok:latest
deploy:
	heroku container:login && \
	heroku container:push web -a utfpr-chatbot
release:
	heroku container:release web -a utfpr-chatbot
# ngrok-docker:
# 	docker run -p 4040:4040 --name ngrok -d -e NGROK_AUTHTOKEN=<token> aurelixv/ngrok:latest http host.docker.internal:5005
ngrok:
	ngrok http 5005 --config ./ngrok/ngrok.yml
clear-bot-cache:
	rm -r bot/.rasa/*
psql:
	heroku pg:psql -a utfpr-chatbot
