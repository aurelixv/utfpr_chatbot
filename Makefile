train:
	cd bot/ && \
	rasa train --fixed-model-name nlu_utfpr_chatbot
run:
	cd bot/ && rasa run -vv --model models/nlu_utfpr_chatbot.tar.gz --credentials credentials_dev.yml
actions:
	cd bot/ && rasa run actions -p 5055
build-bot:
	docker build -t aurelixv/utfpr_chatbot . && \
	docker push aurelixv/utfpr_chatbot:latest
build-ubuntu:
	cd ubuntu/ && \
	docker build -t aurelixv/ubuntu . && \
	docker push aurelixv/ubuntu:latest
deploy:
	heroku container:login && \
	heroku container:push web -a utfpr-chatbot && \
	heroku container:release web -a utfpr-chatbot
ngrok:
	ngrok http 5005
clear:
	rm -r bot/.rasa
