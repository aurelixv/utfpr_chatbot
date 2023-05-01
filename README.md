
<a href="url"><img src="/misc/bot_logo.jpeg" height="auto" width="500"></a>

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

### Tutorial para executar o Chatbot na máquina local:

####0. Pré-requisitos:
- Possuir o Docker instalado na máquina:
    - https://www.docker.com/products/docker-desktop/
- Possuir o ngrok instalado na máquina:
    - https://ngrok.com/download
    - Criar conta e preencher token no arquivo ngrok/ngrok.yml

- **Preferencialmente**: um terminal que consiga executar comandos Makefile. Caso contrário, consultar o arquivo Makefile e rodar os comandos diretamente no terminal, fazendo as adaptações locais necessárias.

#### 1. Clonar o repositório para a máquina local:
```shell
$ git clone https://github.com/aurelixv/utfpr_chatbot
```

#### 2. Treinar modelo:
Obs: Certifique-se que o Docker esteja rodando antes de executar o comando.
```shell
$ make train
```

#### 3. Inicializar o ngrok:
Necessário para abrir a porta 5005 da máquina local para comunicação do Chatbot com o Telegram. Utilizará as configurações presentes no arquivo ngrok/ngrok.yml
```shell
$ make ngrok
# Após rodar, copiar o endereço https e colar no arquivo credentials.yml
```

#### 4. Subir o bot:
Utilizando Docker Compose, sobe os 3 containers necessários para o funcionamento do Chatbot: rasa, rasa-sdk e postgres. As imagens possuem personalizações e estão disponíveis no Docker Hub aurelixv.
```shell
$ make run
```

#### Extra: Subir versão limpa:
Sobe uma versão limpa das imagens Docker, para reinicializar tudo.
```shell
$ make clean
```

### Desenvolvimento local de códigos Python

Para desenvolver códigos locais ou utilizar os notebooks disponíveis no projeto, necessário criar um ambiente virtual do python, conforme passos:

#### 1. Criar venv do python:
```shell
$ python3 -m venv venv
```

#### 2. Ativar venv do python:
```shell
$ source ./venv/bin/activate
```

### Personalização das imagens Docker

Caso seja necessário atualizar ou personalizar alguma das imagens Docker utilizadas no projeto, utilizar os respectivos comandos conforme necessidade:

#### Criar imagem docker do rasa server:
```shell
$ make build-rasa
```

#### Criar imagem docker do actions server:
```shell
$ make build-actions
```

#### Criar imagem docker do postgres:
```shell
$ make build-postgres
```

### Comandos para deploy/release

#### Deploy da aplicação no Heroku:
```shell
$ make deploy
```

#### Release da aplicação no Heroku:
```shell
$ make release
```

#### Para inicializar o postgres do terminal:
```shell
$ heroku pg:psql -a utfpr-chatbot
```

### Misc

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
