# camalot

## Getting started

1. https://docs.docker.com/docker-for-mac/install/

2. `docker volume create <volume-name>`

3. `docker pull postgres`

4. `docker run --rm --name <container-name> -e POSTGRES_PASSWORD=docker -d -p 5432:5432 --mount 'source=<volume-name>,target=/var/lib/postgresql/data' postgres`

5. `python bootstrap_db.py`
