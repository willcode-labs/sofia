# Projeto Sofia

## Introdução

Core para o projeto de sistema integrado de comércio digital.

## Instalação

Na maquina hospedeira, estarão instalados os containers especificos para cada projeto.

### Ambiente

Instalar docker.
https://docs.docker.com/install/linux/docker-ce/debian/

Na pasta container estão disponiveis os ambientes de aplicação(app) e base de dados(database).

#### Base de dados.

Subir container.

1. `docker build --force-rm -t sofia-core-dev-db .`
2. `docker run --name SOFIA-CORE-DEV-DB -p 9001:5432 -e POSTGRES_PASSWORD={{password}} -d {{image}}"`

#### Aplicação.

Subir container.

1. `docker build --force-rm -t sofia-core-dev .`
2. `docker run --name SOFIA-CORE-DEV --link SOFIA-CORE-DB-DEV -p 9002:80 -d {{image}}`

### Pôs-instalação

No container da aplicação SOFIA-CORE-DEV executar os comandos para migração da
base de dados.

1. `python3 makemigrations api --check`
2. `python3 migrate api`

### Testes

* `python3 -Wall manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`
* `coverage run --source='.' manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`
