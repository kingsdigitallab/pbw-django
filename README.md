# pbw-django

The new Django application for the Prosopography of the Byzantine World (PBW).

### Overview

This is the repository for Prosopography of the Byzantine World, currently maintained by [King's Digital Lab](https://github.com/kingsdigitallab/).

This project has been redesigned to run in a Docker container, aimed at an Openstack deployment. 


## Technology
1. Django 3.2.5
2. JQuery
3. MySQL 5.7
4. django-haystack 3.1.1
5. Elasticsearch 7.1


## Containers:

- [nginx-proxy](https://hub.docker.com/r/nginxproxy/nginx-proxy): This is the primary entry point for the stack, running on 80.  It automatically builds a proxy to other containers.
- [django 3.2](https://hub.docker.com/layers/library/python/3.6-slim-buster/images/sha256-5dd134d6d97c67dd02e4642ab24ecbb9d23059ea018a8b5185784d29dce2f37a?context=explore): The main container for the project (see more detailed description below.) 
- [nginx](https://hub.docker.com/_/nginx): This is the static data container, serving Django's static content.
- db: The database container for Django above, running a legacy version of MySQL (5.7).
- elasticsearch [7.10](https://hub.docker.com/_/elasticsearch): The indexing container, used by Haystack 3.2.1. (Pre-migration, Haystack 2 was using Solr 6.)

## ENV file

The compose file will look for deployment variables in a compose/.env file.  Below is a sample file:

```
#Django
DJANGO_READ_DOT_ENV_FILE=True
DJANGO_ALLOWED_HOSTS=
DJANGO_SECRET_KEY=
DJANGO_DEBUG=False

# Elasticsearch
# ------------------------------------------------------------------------------
discovery.type=single-node


# MySQL
# ------------------------------------------------------------------------------
DATABASE_URL=
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_HOST=db

```

Fill in the database credentials and Django variables.  If deploying via a CI pipeling such as Gitlab, this file will need to be included in its variables (in the KDL setup, we encode this in base64 and add it to the CI/CD variables in the repository settings.)

## Getting started
1. Enter the project directory: `cd pbw-django`
2. Build and run the docker containers `docker compose -f compose/docker-compose.yml up -d --build`
3. Copy mysql data into the db container and ingest it via the command line if necessary.
4. **Haystack indexes are not buit during the build process**.  To build the Haystack search indexes, first log into the django container `docker compose -f compose/docker-compose.yml exec django bash`.  Then run the update_index management command: `python manage.py update_index`

You can access the site locally at [http://localhost](http://localhost)