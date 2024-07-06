import os
from dotenv import load_dotenv

APP_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_FILE = '.test_env'

load_dotenv(os.path.join(APP_DIR, ENV_FILE))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError

    PORT = 5050
    HOST = 'localhost'
    DEBUG = False

    API_ELEVATION_TIF_PATH = os.path.join(APP_DIR, './app/data/srtm_N55E160.tif')


class DevelopConfig(BaseConfig):
    DEBUG = True


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProdConfig(BaseConfig):
    DEBUG = False


config = DevelopConfig
