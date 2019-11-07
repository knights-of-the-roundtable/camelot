# camelot

## Getting started

1. https://docs.docker.com/docker-for-mac/install/

2. `docker volume create <volume-name>`

3. `docker pull postgres`

4. `docker run --rm --name <container-name> -e POSTGRES_PASSWORD=docker -d -p 5432:5432 --mount 'source=<volume-name>,target=/var/lib/postgresql/data' postgres`

5. `python bootstrap_db.py`

## Building package with serverless framework

1. `npm install`

2. `serverless deploy --stage dev`

## Building package manually (obsolete)

1. `docker run --rm -v <full-path-src>:/home -w="/home" python:3.7 pip install --target ./package -r requirements.txt`

2. `cd package && zip -r9 ../function.zip . && cd ..`

3. `zip -g function.zip <lambda_file> <dependencies...>`

dependencies will usually include `db_util.py` and `models.py`
