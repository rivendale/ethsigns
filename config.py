"""Application configuration module."""

from os import getenv, path

from pathlib import Path

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
    ADMINS = getenv('ADMINS', [])


class ProductionConfig(Config):
    """App production configuration."""


class DevelopmentConfig(Config):
    """App development configuration."""

    SQLALCHEMY_DATABASE_URI = getenv(
        'DATABASE_URL', 'sqlite:///' + path.join(basedir, 'ethsigns.db'))
    AUTH_URL = getenv('AUTH_URL_STAGING')
    DEBUG = True


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
}

AppConfig = config.get(getenv('FLASK_ENV',  'development'))
