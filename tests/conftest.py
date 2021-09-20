import asyncio
import os
from types import SimpleNamespace

import pytest
from alembic.command import upgrade
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from movie_app.__main__ import parser
from movie_app.api.app import create_app
from movie_app.constants import Templates
from movie_app.utils.pg import make_alembic_config


def delete_db(tmp_url):
    """Удаление БД, если такая существует"""
    if database_exists(tmp_url):
        drop_database(tmp_url)


@pytest.fixture(scope="session")
def postgres():
    """Создает временную БД для запуска теста."""
    tmp_url = os.environ["POSTGRES_DB_URL"]

    # Может быть так, что тесты пошли не по плану и БД не удалена,
    # тогда нужно удалить принудительно
    delete_db(tmp_url)
    create_database(tmp_url)

    try:
        yield tmp_url
    finally:
        delete_db(tmp_url)


@pytest.fixture(scope="session")
def alembic_config(postgres):
    """Создает объект с конфигурацией для alembic, настроенный на временную БД."""
    cmd_options = SimpleNamespace(
        config="alembic.ini", name="alembic", pg_url=postgres, raiseerr=False, x=None
    )
    return make_alembic_config(cmd_options)


@pytest.fixture(scope="session")
async def migrated_postgres(alembic_config, postgres):
    """Возвращает URL к БД с примененными миграциями."""
    upgrade(alembic_config, "head")
    return postgres


@pytest.fixture()
def arguments(aiomisc_unused_port, migrated_postgres):
    """Аргументы для запуска приложения."""
    return parser.parse_args(
        [
            "--log-level=info",
            "--api-address=127.0.0.1",
            f"--api-port={aiomisc_unused_port}",
            f"--pg-url={migrated_postgres}",
        ]
    )


@pytest.fixture()
async def api_client(aiohttp_client, arguments):
    """Заводим клиента"""
    app = create_app(arguments)
    client = await aiohttp_client(app, server_kwargs={"port": arguments.api_port})

    try:
        yield client
    finally:
        await client.close()


@pytest.fixture(scope="session")
async def migrated_postgres_connection(migrated_postgres):
    """Синхронное соединение со смигрированной БД."""
    engine = create_engine(migrated_postgres)
    async with engine.connect() as conn:
        yield conn


@pytest.fixture(scope="session")
async def async_conn(migrated_postgres):
    """Асинхронное соединение со смигрированной БД."""
    engine = create_async_engine(Templates.ASYNC_CONNECTION_URL)

    async with AsyncSession(engine) as session:
        async with session.begin():
            yield session

        await session.commit()


@pytest.fixture(scope="session")
def loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
