INTERNAL_IPS = ('0.0.0.0', '127.0.0.1', '::1')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%5@l_k_=161v!k7$oe%4hw6khybi5x@5ct32sx95+#keb-#x)j'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pbw-django',
        'USER': 'app_pbw',
        'PASSWORD': 'pbw',
       # 'HOST': 'my-stg-1.cch.kcl.ac.uk',
        'PORT': '3306',
        'HOST': 'localhost',


    }
}

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'chopin.settings.local.show_toolbar',
}

# https://github.com/sehmaschine/django-grappelli/issues/456
# Any value other than "" in the setting value will break the inline templates
TEMPLATE_STRING_IF_INVALID = 'INVALID %s'