from .base import *  # noqa

#CACHE_REDIS_DATABASE = '2'
#CACHES['default']['LOCATION'] = '127.0.0.1:6379:' + CACHE_REDIS_DATABASE

DEBUG = env.bool("DJANGO_DEBUG", False)


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['pbw-os.kdl.kcl.ac.uk'])

INTERNAL_IPS = ['0.0.0.0', '127.0.0.1', '::1', '10.0.2.2']

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'NAME': env("MYSQL_DATABASE"),
        'USER': env("MYSQL_USER"),
        'PASSWORD': env("MYSQL_PASSWORD"),
        'HOST': env("MYSQL_HOST")

    },
}

