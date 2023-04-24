## Chatbot para a UTFPR
#### Trabalho de Conclusão de Curso - Bacharelado em Sistemas de Informação - UTFPR
#### Autor:  Aurélio Vinícius Cabral Funes

#### Tecnologias Utilizadas:
- Rasa Open Source
- Rasa Actions Server
- Python
- Git
- Docker
- Docker Compose
<!-- - Heroku -->
- Postgres

#### Criar imagem docker do rasa server:
```shell
make build-rasa
```

#### Criar imagem docker do actions server:
```shell
make build-actions
```

#### Criar imagem docker do postgres:
```shell
make build-postgres
```

#### Treinar modelo:
```shell
make train
```

#### Subir o bot:
```shell
make run
```

#### Subir versão limpa:
```shell
make clean
```

#### Deploy da aplicação no Heroku:
```shell
make deploy
```

#### Release da aplicação no Heroku:
```shell
make release
```

#### Deploy local conectando ao telegram:
```shell
make ngrok
# Após rodar, copiar o endereço https e colar no arquivo credentials.yml
```

#### Para inicializar o postgres do terminal:
```shell
heroku pg:psql -a utfpr-chatbot
```

#### Para criar as bases no postgres (**DDL**):
```shell
# Utilizar códigos .sql para criar as tabelas, presentes em /postgres/DDL 
# Durante o build da imagem do postgres, os códigos e a carga são chamados pelo script /postgres/ingestion.sh
```

#### Para preencher as bases criadas (**DML**):
1. Criar scripts de carga
1. Rodar scripts como o passo anterior

**OU**

1. Abrir o pgAdmin4
1. Conectar no database
1. Ir na Tabela **>** Import/Export Data...
1. Selecionar arquivo **.csv** que deseja importar
1. Options **>** Ativar opção Header **>** Alterar Delimiter para '**;**'

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
