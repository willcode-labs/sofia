# Projeto Sofia

## Introdução

Core para o projeto de sistema integrado de comércio digital.

## Instalação

Instalar GIT.
https://git-scm.com/download/linux

Efetuar o clone do projeto.

1. `$ git clone {{REPO-URL}}`

### Dependencias

Instalar docker.
https://docs.docker.com/install/linux/docker-ce/debian/

Dependencias da aplicação ou do framework.

1. `$ pip3 install -r requirements.txt`

Dependencias da base de dados.

1. `$ docker image pull postgres:latest`
2. `$ docker run --name SOFIA-CORE-{{ENVIRONMENT}} -p {{DB-POST}}:5432 -e POSTGRES_PASSWORD={{PASSWORD}} -d postgres`
3. `$ mkdir /data && chmod -R 777 /data`
4. `$ chown postgres /data`
5. `$ su postgres`
6. `$ psql`
7. `$ CREATE TABLESPACE sofia_core_{{ENVIRONMENT}} OWNER postgres LOCATION '/data';`
8. `$ CREATE DATABASE sofia_core_development OWNER postgres TABLESPACE sofia_core_development;`
9. `$ \q`

Roda os comandos para migração das tabelas e dados.

1. `$ python3 makemigrations api --check`
2. `$ python3 migrate api`

### Testes

* `$ python3 -Wall manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`
* `$ coverage run --source='.' manage.py test api.test --failfast --keepdb --settings api.test.testsSettings -v 3`
