
<a href="url"><img src="/misc/bot_logo.jpeg" height="auto" width="500"></a>

## Chatbot para a UTFPR
#### Trabalho de Conclusão de Curso - Bacharelado em Sistemas de Informação - UTFPR
#### Autor:  Aurélio Vinícius Cabral Funes

## Índice
- [Chatbot para a UTFPR](#chatbot-para-a-utfpr)
    - [Trabalho de Conclusão de Curso - Bacharelado em Sistemas de Informação - UTFPR](#trabalho-de-conclusão-de-curso---bacharelado-em-sistemas-de-informação---utfpr)
    - [Autor:  Aurélio Vinícius Cabral Funes](#autor--aurélio-vinícius-cabral-funes)
- [Índice](#índice)
    - [Tecnologias Utilizadas](#tecnologias-utilizadas)
  - [Tutorial para executar o Chatbot na máquina local ou em máquina virtual](#tutorial-para-executar-o-chatbot-na-máquina-local-ou-em-máquina-virtual)
    - [0. Pré-requisitos](#0-pré-requisitos)
    - [Máquina Local](#máquina-local)
    - [Máquina Virtual (Ubuntu 22.04)](#máquina-virtual-ubuntu-2204)
    - [1. Clonar o repositório](#1-clonar-o-repositório)
    - [2. Preencher credenciais necessárias](#2-preencher-credenciais-necessárias)
    - [3. Treinar modelo (opcional)](#3-treinar-modelo-opcional)
    - [4. Inicializar o ngrok](#4-inicializar-o-ngrok)
    - [5. Subir e parar o bot](#5-subir-e-parar-o-bot)
    - [Extra: Subir versão limpa](#extra-subir-versão-limpa)
  - [Alterando credenciais do Telegram](#alterando-credenciais-do-telegram)
    - [Conversando com o Chatbot](#conversando-com-o-chatbot)
  - [Utilizando o pgadmin para atualizar dados](#utilizando-o-pgadmin-para-atualizar-dados)
  - [Desenvolvimento local de códigos Python](#desenvolvimento-local-de-códigos-python)
    - [1. Criar venv do python](#1-criar-venv-do-python)
    - [2. Ativar venv do python](#2-ativar-venv-do-python)
    - [3. Instalar pacotes](#3-instalar-pacotes)
  - [Personalização das imagens Docker](#personalização-das-imagens-docker)
    - [Criar imagens docker do rasa server, actions server, postgres e pgadmin:](#criar-imagens-docker-do-rasa-server-actions-server-postgres-e-pgadmin)
  - [Misc](#misc)
    - [Para criar as bases no postgres (**DDL**)](#para-criar-as-bases-no-postgres-ddl)
    - [Para preencher as bases criadas (**DML**)](#para-preencher-as-bases-criadas-dml)
    - [Git ignorar alteraçōes nos arquivos](#git-ignorar-alteraçōes-nos-arquivos)
    - [Git remover commits antigos em arquivos (credenciais)](#git-remover-commits-antigos-em-arquivos-credenciais)


#### Tecnologias Utilizadas
- Rasa Open Source
- Rasa Actions Server
- Python
- Git
- Docker
- Docker Compose
- Postgres

### Tutorial para executar o Chatbot na máquina local ou em máquina virtual

#### 0. Pré-requisitos
#### Máquina Local
- Possuir o Docker Desktop instalado:
    - https://www.docker.com/products/docker-desktop/
- Possuir o ngrok instalado:
    - https://ngrok.com/download
    - Criar conta e preencher token no arquivo ngrok/ngrok.yml
- Possuir o Python instalado
    - https://www.python.org/downloads/
- **Preferencialmente**: um terminal que consiga executar comandos Makefile. Caso contrário, consultar o arquivo Makefile e rodar os comandos diretamente no terminal, fazendo as adaptações locais necessárias.

#### Máquina Virtual (Ubuntu 22.04)
- Instalação de Docker e Docker Compose:
    - https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04
    - https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04
- Possuir o ngrok instalado:
    - https://ngrok.com/
    - Criar conta e preencher token no arquivo ngrok/ngrok.yml
    - Rodar o seguinte comando para instalar:
    ```shell
    $ sudo snap install ngrok
    ```
- Instalar o make
    ```shell
      $ sudo apt install make
    ```
- Instalar o Python
  ```shell
    $ sudo apt install python-is-python3
  ```

#### 1. Clonar o repositório
```shell
$ git clone https://github.com/aurelixv/utfpr_chatbot
```

Se desejar treinar um modelo, é necessário alterar o grupo da pasta **bot** para root, com o comando abaixo:
```shell
$ sudo chgrp -R bot root
```

#### 2. Preencher credenciais necessárias
- Substituir texto **\<token\>** do campo do arquivo pela correspondente chave de acesso
- **bot/credentials.yml**: preencher com o token de acesso do Telegram
- **ngrok/ngrok.yml**: preencher com o token de acesso do ngrok

#### 3. Treinar modelo (opcional)
Obs: Certifique-se que o Docker esteja rodando antes de executar o comando.
```shell
$ make train
```

#### 4. Inicializar o ngrok
Necessário para abrir a porta 5005 da máquina local para comunicação do Chatbot com o Telegram. Utilizará as configurações presentes no arquivo ngrok/ngrok.yml
```shell
$ make ngrok
```

Após, rodar o seguinte comando para atualizar o endereço gerado pelo ngrok:
```shell
$ make update-webhook
```

Ao terminar de utilizar a conexão, rodar o seguinte comando para desconectar sessão:
```shell
$ killall ngrok
```

#### 5. Subir e parar o bot
Utilizando Docker Compose, sobe os containers necessários para o funcionamento do Chatbot: rasa, rasa-sdk, postgres e pgadmin. As imagens possuem personalizações e estão disponíveis no Docker Hub aurelixv.
```shell
# Subir o bot
$ make up
```

```shell
# Parar o bot
$ make stop
```

```shell
# Apaga containers
$ make down
```

#### Extra: Subir versão limpa
Sobe uma versão limpa das imagens Docker, para reinicializar tudo.
```shell
$ make clean
```

### Alterando credenciais do Telegram

#### Conversando com o Chatbot

### Utilizando o pgadmin para atualizar dados

### Desenvolvimento local de códigos Python

Para desenvolver códigos locais ou utilizar os notebooks disponíveis no projeto, necessário criar um ambiente virtual do python, conforme passos:

#### 1. Criar venv do python
```shell
$ python3.10 -m venv venv
```

#### 2. Ativar venv do python
```shell
$ source ./venv/bin/activate
```

#### 3. Instalar pacotes
```shell
$ pip install -r requirements.txt
```

### Personalização das imagens Docker

Caso seja necessário atualizar ou personalizar alguma das imagens Docker utilizadas no projeto, alterar arquivo **docker-compose.yml** para respectiva conta Docker Hub (ou nenhuma conta) e utilizar o respectivo comando:

#### Criar imagens docker do rasa server, actions server, postgres e pgadmin:
```shell
$ make build
```

### Misc

#### Para criar as bases no postgres (**DDL**)
```shell
# Utilizar códigos .sql para criar as tabelas, presentes em /postgres/DDL 
# Durante o build da imagem do postgres, os códigos e a carga são chamados pelo script /postgres/ingestion.sh
```

#### Para preencher as bases criadas (**DML**)
1. Criar scripts de carga
1. Rodar scripts como o passo anterior

**OU**

1. Abrir o pgAdmin4
1. Conectar no database
1. Ir na Tabela **>** Import/Export Data...
1. Selecionar arquivo **.csv** que deseja importar
1. Options **>** Ativar opção Header **>** Alterar Delimiter para '**;**'

#### Git ignorar alteraçōes nos arquivos
```shell
# parar
git update-index --skip-worktree <file>

# voltar
git update-index --no-skip-worktree <file>
```

#### Git remover commits antigos em arquivos (credenciais)
```shell
git filter-branch --index-filter \                
    'git rm -rf --cached --ignore-unmatch <file>' HEAD
```
