import os

from dotenv import load_dotenv

load_dotenv()


class Templates(object):
    """Шаблоны базовых строк, которые необходимы в процессе эксплуатации."""

    ASYNC_CONNECTION_URL = (
        f"postgresql+asyncpg://{os.environ.get('POSTGRES_DB_URL').split('://')[1]}"
    )
