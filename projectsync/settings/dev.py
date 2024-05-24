from .base import *



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'asyncdb',      
        'USER': 'postgres',
        'PASSWORD': 'psql', 
        'HOST': 'localhost',
        'PORT': '5432', 
    }
}