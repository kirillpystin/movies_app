import csv
from collections import defaultdict

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from app.constants import Templates
from sqlalchemy.pool import NullPool


class Core(object):
    """Ядро приложения. Осуществляет все базовые операции."""

    engine = create_async_engine(
        Templates.ASYNC_CONNECTION_URL, echo=True, poolclass=NullPool
    )

    # Модель
    model = None

    # Схема валидации
    schema = None

    # Таблица в БД
    table = None

    # Число записей на странице
    paginate_count = 100

    session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    @staticmethod
    def read_csv(films_csv):
        """Чтение фильмов из файла.

        Args:
            films_csv(str): Файл с фильмом.
        """
        list_of_films = []
        with open(films_csv, "r") as file:
            my_reader = csv.reader(file, delimiter=",")
            rows = tuple(my_reader)
            titles = rows[0]

            for row in rows[1:]:
                item = defaultdict(dict)
                for idx, itm in enumerate(titles):
                    item[itm] = row[idx]

                list_of_films.append(item)

        return list_of_films

    @classmethod
    async def add_records(cls, records):
        """Добавление всех записей в таблицу.

        Args:
            records(list): Список записей на добавление
        """
        async with cls.session() as session:
            session.add_all(records)
            await session.commit()

    @classmethod
    async def get_record(cls, record_id):
        """Извлечение записи из таблицы.

        Args:
            record_id(str): id записи
        """
        record_id = int(record_id)

        async with cls.session() as session:
            record = await session.get(cls.model, record_id)

        return cls.schema.dump(record)

    @classmethod
    async def create(cls, **params):
        """Создание записи в БД.

        Args:
            params(dict): Параметры, для создания записи
        """
        async with cls.session() as session:
            session.add(cls.model(**params))

    @classmethod
    async def get_list(cls, page_number):
        """Извлечение списка записей постранично.

        Args:
            page_number: номер страницы

        Returns:
            list: Список извлеченных объъектов

        """
        page_number = int(page_number)

        async with cls.session() as session:
            result = await session.execute(
                select(cls.model)
                .offset(cls.paginate_count * page_number)
                .limit(cls.paginate_count)
            )
            result = [a1 for a1 in result.scalars()]

        return cls.schema.dump(result, many=True)

    @classmethod
    async def get_by(cls, **kwargs):
        """Извлечение записи с заданным филтром.

        Args:
            kwargs: параметры запроса

        Returns:
            list: Список извлеченных объъектов

        """
        async with cls.session() as session:
            result = await session.execute(
                select(cls.model)
                .filter_by(**kwargs)
                .limit(1)
            )
            result = [a1 for a1 in result.scalars()][0]

        return result

    @classmethod
    async def get_all(cls, **kwargs):
        """Извлечение массива записей.

        Args:
            kwargs: параметры запроса

        Returns:
            list: Список извлеченных объъектов

        """
        async with cls.session() as session:
            result = await session.execute(
                select(cls.model)
                .filter_by(**kwargs)
            )
            result = [a1 for a1 in result.scalars()]

        return result

    @classmethod
    async def delete(cls, record_id):
        """Удаление записи.

        Args:
            record_id(int): идентификатор записи.

        """
        async with cls.session() as session:
            record = await session.get(cls.model, int(record_id))
            await session.delete(record)
            await session.commit()

    @classmethod
    async def update(cls, **kwargs):
        """Обновление записи.

        Args:
            kwargs(dict): Параметры для обновления.
        """
        record_id = kwargs.pop("id")

        async with cls.session() as session:
            await session.execute(
                update(cls.table)
                .where(cls.table.c.id == record_id)
                .values(**kwargs)
            )
            await session.commit()
        await cls.engine.dispose()
