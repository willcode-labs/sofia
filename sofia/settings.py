import os,datetime,sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '27r3kq0e4qbr7kks!h&cqt^t5)9$oudecl6dr4!h_(_#)73^g+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    'api.Middleware.MethodNotAllowed.MethodNotAllowed',
    'api.Middleware.Rest.Rest',
]

ROOT_URLCONF = 'sofia.urls'

TEMPLATES = []

WSGI_APPLICATION = 'sofia.wsgi.application'

# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sofia_core_development',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '8092',
        'TEST' : {
            'NAME': 'sofia_core_test',
        }
    },
    # 'test': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.dev.sqlite3'),
    #     'TEST' : {
    #         'NAME': 'db.test.sqlite3',
    #     }
    # },
}

# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Brazil/East'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = None

# https://docs.djangoproject.com/en/1.11/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(name)s|%(levelname)s|%(asctime)s|%(module)s|%(pathname)s|%(filename)s LINE(%(lineno)d)|%(funcName)s|%(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'file_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'log/WARNING.log'),
            'when': 'midnight',
            'formatter': 'verbose'
        },
        'file_critical': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'log/CRITICAL.log'),
            'when': 'midnight',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'sofia.api.debug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'sofia.api.warning': {
            'handlers': ['file_warning','console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'sofia.api.critical': {
            'handlers': ['file_critical','console'],
            'level': 'CRITICAL',
            'propagate': True,
        }
    }
}
