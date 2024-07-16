import os
from dotenv import load_dotenv

APP_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_FILE = '.env'

load_dotenv(os.path.join(APP_DIR, ENV_FILE))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError

    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')
    DEBUG = False
    TESTING = False

    APP_DIR = APP_DIR

    STATIC_URL = ''
    STATIC_DIR = os.path.join(APP_DIR, './frontend/dist')

    API_ELEVATION_TIF_PATH = os.path.join(APP_DIR, './app/data/srtm_N55E160.tif')


class DevelopConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProdConfig(BaseConfig):
    DEBUG = False


config = ProdConfig
