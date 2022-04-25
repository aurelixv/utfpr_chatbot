train:
	cd bot/ && \
	rasa train --fixed-model-name nlu_utfpr_chatbot
run:
	cd bot/ && rasa run -vv --model models/nlu_utfpr_chatbot.tar.gz
	# docker run -p 5005:5005 utfpr_chatbot
build:
	docker build -t utfpr_chatbot .
deploy:
	heroku container:login && \
	heroku container:push web -a utfpr-chatbot && \
	heroku container:release web -a utfpr-chatbot
ngrok:
	ngrok http 5005