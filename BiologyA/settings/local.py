from .base import *

DEBUG = True

# DATABASES = {
#     'default':
#         {'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': BASE_DIR / 'db.sqlite3',}
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biology',
        'USER': 'zsprawl',
        'PASSWORD': 'HPM0ZS6VU8',
    }
}