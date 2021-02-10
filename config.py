"""Application configuration module."""

import sys
from os import getenv, path

from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """App base configuration."""
    SECRET_KEY = getenv('SECRET_KEY', '')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL',
                                     'sqlite:///' + path.join(basedir, 'ethsigns.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    DEBUG = False
    LOG_TO_STDOUT = getenv('LOG_TO_STDOUT', True)
    API_BASE_URL_V1 = getenv('API_BASE_URL_V1', "")
    ADMINS = getenv('ADMINS', [])


class ProductionConfig(Config):
    """App production configuration."""


class DevelopmentConfig(Config):
    """App development configuration."""

    SQLALCHEMY_DATABASE_URI = getenv(
        'DATABASE_URL', 'sqlite:///' + path.join(basedir, 'ethsigns.db'))
    AUTH_URL = getenv('AUTH_URL_STAGING')
    DEBUG = True


class TestingConfig(Config):
    """App testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv(
        'TEST_DATABASE_URL',
        default='sqlite:///' + path.join(basedir, 'ethsigns-test.db'))
    FLASK_ENV = 'testing'
    API_BASE_URL_V1 = "/api/v1"
    WTF_CSRF_ENABLED = False


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}

AppConfig = TestingConfig if 'pytest' in sys.modules else config.get(
    getenv('FLASK_ENV', 'development'))
