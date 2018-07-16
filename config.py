APP_NAME = 'vod_history'


class BaseConfig:
    PROJECT = 'FPTPLAY_CRAWLER'


class DevConfig(BaseConfig):
    DEBUG = True

    # ============== APP =============================
    WEB_APP_HOST = '0.0.0.0'
    WEB_APP_POST = 5005

    # ============== REDIS POST ======================
    REDIS_HOST = "localhost"
    REDIS_POST = 6379


