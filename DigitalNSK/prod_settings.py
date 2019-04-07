STATIC_ROOT = "/var/www/www-root/data/www/api.digitalnsk.sibtiger.com/static"
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = "/var/www/www-root/data/www/api.digitalnsk.sibtiger.com/media"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'digitalnsk',
        'USER': 'digitalnsk',
        'PASSWORD': 'Sibtigernstu2017',
        'HOST': '178.21.10.142',
        'PORT': '5432',
    }
}