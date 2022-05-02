## Chatbot para a UTFPR
#### Trabalho de Conclusão de Curso - Bacharelado em Sistemas de Informação - UTFPR
#### Autor:  Aurélio Vinícius Cabral Funes

#### Tecnologias Utilizadas:
- Rasa Open Source
- Rasa Actions Server
- Python
- Git
- ngrok
- Docker
- Heroku
- Postgres

#### Iniciar venv:
```shell
source ./venv/bin/activate
```

#### Treinar modelo:
```shell
make train
```

#### Subir o bot:
```shell
make run
```

#### Subir o actions server:
```shell
make actions
```

#### Build da aplicação com Docker:
```shell
make build-bot
```

#### Deploy da aplicação no Heroku:
```shell
make build-bot
```

#### Deploy local conectando ao telegram:
```shell
ngrok http 5005
# Após rodar, copiar o endereço https e colar no arquivo credentials.yml
```

#### Para inicializar o postgres do terminal:
```shell
heroku pg:psql -a utfpr-chatbot
```

#### Para criar as bases no postgres do terminal:
```shell
heroku pg:psql -a utfpr-chatbot
\i postgres/DDL/CAMPI.sql
\i postgres/DDL/PHASE.sql
\i postgres/DDL/ENROLLMENT_SCHEDULE.sql
```

#### Git ignorar alteraçōes nos arquivos:
```shell
# parar
git update-index --skip-worktree <file>

# voltar
git update-index --no-skip-worktree <file>
```

#### Git remover commits antigos em arquivos (credenciais):
```shell
git filter-branch --index-filter \                
    'git rm -rf --cached --ignore-unmatch <file>' HEAD
```
