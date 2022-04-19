## Chatbot para a UTFPR
#### Trabalho de Conclusão de Curso - Bacharelado em Sistemas de Informação - UTFPR
#### Autor:  Aurélio Vinícius Cabral Funes

#### Tecnologias Utilizadas:
- Rasa NLU
- Rasa Core
- Python
- Git
- ngrok
- Docker
- Heroku 

#### Iniciar venv:
```shell
source ./venv/bin/activate
```

#### Treinar modelo:
```shell
make train
```

#### Subir ambiente:
```shell
make run
```

#### Deploy local conectando ao telegram:
```shell
ngrok http 5005
# Após rodar, copiar o endereço https e colar no arquivo credentials.yml
```
