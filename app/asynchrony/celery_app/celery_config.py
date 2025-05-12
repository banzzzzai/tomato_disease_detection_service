from functools import lru_cache

import config


class BaseConfig:
    broker_url: str = config.CELERY_BROKER_URL

    result_backend: str = config.CELERY_RESULT_BACKEND
    timezone: str = "Europe/Moscow"
    # timezone: str = "UTC"
    result_expires: int = int(config.CELERY_RESULT_EXPIRE)
    enable_utc = True
    broker_connection_retry_on_startup = True
    task_track_started = True
    include = ['asynchrony.tasks']
    worker_concurrency = 10


class DevelopConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "production": DevelopConfig,
        "development": DevelopConfig,
    }

    config_name = config.CELERY_CONFIG
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
