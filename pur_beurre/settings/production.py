from . import *

SECRET_KEY = '-~aO;| F;rE[??/w^zcumh(9'
DEBUG = False
ALLOWED_HOSTS = ['192.168.10.41']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'pur_beurre', # le nom de notre base de données créée précédemment
        'USER': 'zelix', # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'Azerty',
        'HOST': '',
        'PORT': '5432',
    }
}


