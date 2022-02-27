import os

# La configuracion de la base de datos
DATABASES_CONFIG = {
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'db.sqlite3'),
    },
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medios_basicos',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'medios_basicos',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
    'mongodb': {
        'ENGINE': 'djongo',
        'NAME': 'medios_basicos',
        # 'ENFORCE_SCHEMA': False,
        # 'CLIENT': {
        #    'host': 'host-name or ip address',
        #    'port': port_number,
        #    'username': 'db-username',
        #    'password': 'password',
        #    'authSource': 'db-name',
        #    'authMechanism': 'SCRAM-SHA-1'
        # },
        # 'LOGGING': {
        #    'version': 1,
        #    'loggers': {
        #        'djongo': {
        #            'level': 'DEBUG',
        #            'propagate': False,
        #        }
        #    },
        # },
    },
    'redis': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "medios"
    },
}
