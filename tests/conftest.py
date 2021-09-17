import asyncio
import os
from types import SimpleNamespace

import pytest
from alembic.command import upgrade
from messenger.__main__ import parser
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, drop_database

from messenger.api.app import create_app
from messenger.utils.pg import make_alembic_config


@pytest.fixture(scope="session")
def postgres():
    """
    Создает временную БД для запуска теста.
    """
    tmp_url = os.environ["TEST_DB"]

    try:
        create_database(tmp_url)
    except:
        drop_database(tmp_url)
        create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        drop_database(tmp_url)


@pytest.fixture(scope="session")
def alembic_config(postgres):
    """Создает объект с конфигурацией для alembic, настроенный на временную БД."""
    cmd_options = SimpleNamespace(
        config="alembic.ini", name="alembic", pg_url=postgres, raiseerr=False, x=None
    )
    return make_alembic_config(cmd_options)


@pytest.fixture(scope="session")
async def migrated_postgres(alembic_config, postgres):
    """
    Возвращает URL к БД с примененными миграциями.
    """
    upgrade(alembic_config, "head")
    return postgres


@pytest.fixture
def arguments(aiomisc_unused_port, migrated_postgres):
    """Аргументы для запуска приложения."""
    return parser.parse_args(
        [
            "--log-level=debug",
            "--api-address=127.0.0.1",
            f"--api-port={aiomisc_unused_port}",
            f"--pg-url={migrated_postgres}",
        ]
    )


@pytest.fixture()
async def api_client(aiohttp_client, arguments):
    app = create_app(arguments)
    client = await aiohttp_client(app, server_kwargs={"port": arguments.api_port})

    try:
        yield client
    finally:
        await client.close()


@pytest.fixture(scope="session")
async def migrated_postgres_connection(migrated_postgres):
    """
    Синхронное соединение со смигрированной БД.
    """
    engine = create_engine(migrated_postgres)
    async with engine.connect() as conn:
        yield conn


@pytest.fixture(scope="session")
async def async_conn(migrated_postgres):
    """
    Асинхронное соединение со смигрированной БД.
    """
    url = f"postgresql+asyncpg://{os.environ['TEST_DB'].split('://')[1]}"
    engine = create_async_engine(url)

    async with AsyncSession(engine) as session:
        async with session.begin():
            yield session

        await session.commit()


@pytest.fixture(scope="session")
async def async_session(migrated_postgres):
    """
    Асинхронное соединение со смигрированной БД.
    """
    url = f"postgresql+asyncpg://{os.environ['TEST_DB'].split('://')[1]}"
    engine = create_async_engine(url)

    yield engine


@pytest.fixture(scope="session")
def loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
