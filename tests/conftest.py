"""Module for setting up fixtures for testing"""
# pylint: skip-file
from os import environ

import alembic.command
import alembic.config
# Third-party libraries
import pytest
# Database
from app import app as flask_app
from app import db
from flask import current_app
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (DropConstraint, DropTable, ForeignKeyConstraint,
                               MetaData, Table)

environ['FLASK_ENV'] = 'testing'

pytest_plugins = [
    "tests.fixtures.signs",
]


@pytest.fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.
    :return: Flask app
    """

    _app = flask_app

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='module')
def headers():
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


@pytest.fixture(scope='module')
def init_db(app):
    db.drop_all()
    db.create_all()
    yield db
    db.session.close()
    db.drop_all()


@pytest.fixture(scope='module')
def request_ctx():
    """
    Setup a request client, this gets executed for each test module.
    :param app: Pytest fixture
    :return: Flask request client
    """
    ctx = current_app.test_request_context()
    ctx.push()
    yield ctx
    ctx.pop()


@pytest.fixture(scope="function")
def set_up_db(app):
    # reset database at beginning of test
    db_drop_all(db)
    alembic_cfg = alembic.config.Config('migrations/alembic.ini')
    alembic.command.stamp(alembic_cfg, 'base')

    yield
    # clean database at end of test
    db.session.close()
    db_drop_all(db)


def db_drop_all(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []

        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(ForeignKeyConstraint((), (), name=fk['name']))
        t = Table(table_name, metadata, *fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))
    trans.commit()

    db.engine.execute("DROP TABLE IF EXISTS alembic_version")
