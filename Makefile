train:
	cd bot/ && \
	rasa train --fixed-model-name nlu_utfpr_chatbot
run:
	cd bot/ && rasa run -vv --model models/nlu_utfpr_chatbot.tar.gz --credentials credentials_dev.yml
	# cd bot/ && (rasa run actions -p 5055 & rasa run -vv --model models/nlu_utfpr_chatbot.tar.gz --credentials credentials_dev.yml)
	# docker run -p 5005:5005 utfpr_chatbot
actions:
	cd bot/ && rasa run actions -p 5055
build:
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
