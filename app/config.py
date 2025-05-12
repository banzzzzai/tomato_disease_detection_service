import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv('.env')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
            'datefmt': "%Y/%b/%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'INFO',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        'recognition_service_log': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery_log': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Celery
CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://redis-server:6379/0")
CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://redis-server:6379/0")
CELERY_RESULT_EXPIRE: str = os.getenv("CELERY_RESULT_EXPIRE", 43200)
CELERY_CONFIG: str = os.getenv("CELERY_CONFIG", "production")

REDIS_HOST: str = os.getenv("REDIS_HOST", "redis-server")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

LOGLEVEL: str = os.getenv("LOGLEVEL", "ERROR")

HOST_PROJECT_ROOT: str = os.getenv("HOST_PROJECT_ROOT", '')

