import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_SERVIDOR = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x5$p1g&$ezsv*y0e9datzesr^lpnz#n)yk!p%((_njib7r+9y8'
DEBUG = True

ALLOWED_HOSTS = ['*']

 
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrapform',
    'general',
    'solicitud',
    'administrador',
    'internas',
    'privadas',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RRHH.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                os.path.join(BASE_DIR, 'general', 'templates'),
                os.path.join(BASE_DIR, 'solicitud', 'templates'),
                os.path.join(BASE_DIR, 'administrador', 'templates'),
                ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'RRHH.wsgi.application'

 
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'RRHH',                      # Or path to database file if using sqlite3.
        'USER': 'userRRHH',                      # Not used with sqlite3.
        'PASSWORD': 'Temporal1',                  # Not used with sqlite3.
        'HOST': 'adsysdev\sql2012',
        'OPTIONS': {
            'unicode_results': True,
            'extra_params': 'tds_version=8.0'
        },
    }
}
# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SESSION_COOKIE_AGE = 30 * 60 
# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False
 
 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATIC_URL = '/assets/'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'assets'),
# )

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = '192.168.1.50:25'
EMAIL_HOST_USER = 'ReclutamientoBanrural@banrural.com.hn'
EMAIL_PORT = 587


import django
django.setup()
