"""Application configuration module."""

import sys
from os import getenv, path

from dotenv import load_dotenv
from web3 import Web3, middleware
# from web3.gas_strategies.time_based import fast_gas_price_strategy
# from web3.gas_strategies.rpc import rpc_gas_price_strategy


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """App base configuration."""
    SECRET_KEY = getenv('SECRET_KEY', 'defaultsecretkeytoavoidvirtualtservererrors@##')
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL',
                                     'sqlite:///' + path.join(basedir, 'ethsigns.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    DEBUG = False
    LOG_TO_STDOUT = getenv('LOG_TO_STDOUT', True)
    API_BASE_URL_V1 = getenv('API_BASE_URL_V1', "")
    ADMINS = getenv('ADMINS', [])
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RPC_URL = getenv('RPC_URL', "")
    CONTRACT_ADDRESS = getenv('CONTRACT_ADDRESS', "")
    PRIVATE_KEY = getenv('PRIVATE_KEY', "")
    IPFS_GATEWAY_URL = getenv('IPFS_GATEWAY_URL', "")
    IPFS_API_KEY = getenv('IPFS_API_KEY', "")
    IPFS_URL = getenv('IPFS_URL', "")
    REDIS_URL = getenv('REDIS_URL', 'redis://localhost:6379/0')
    worker_pool_restarts = True
    CELERY_ENABLE_UTC = False
    USE_TZ = True
    CELERY_BROKER_URL = getenv(
        'CELERY_BROKER_URL', 'redis://localhost:6379/0')
    result_backend = getenv(
        'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    web3 = None
    MINTING_FEE = getenv('MINTING_FEE', 0.005503)
    MAX_TOKEN_COUNT = float(getenv('MAX_TOKEN_COUNT', 1000))


class ProductionConfig(Config):
    """App production configuration."""


class DevelopmentConfig(Config):
    """App development configuration."""

    if 'pytest' not in sys.modules:
        # from web3.auto.infura import w3
        # public_address = "0xb55b7719819202b7eF036E664CBC129B657A0c45"
        web3 = Web3(Web3.HTTPProvider(Config.RPC_URL))
        # import pdb
        # pdb.set_trace()
        # web3.eth.getTransactionCount(public_address, "latest")

        web3.middleware_onion.inject(middleware.geth_poa_middleware,  layer=0)

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
