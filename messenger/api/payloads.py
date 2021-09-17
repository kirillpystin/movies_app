import json
from datetime import date
from decimal import Decimal
from functools import partial, singledispatch

from aiohttp.payload import JsonPayload as BaseJsonPayload
from aiohttp.payload import Payload
from asyncpg import Record


@singledispatch
def convert(value):
    """Дженерик-функция для определения типа. Если тип не определен - исключение."""
    raise TypeError(f"Unserializable value: {value!r}")


@convert.register(Record)
def convert_asyncpg_record(value: Record):
    """Позволяет автоматически сериализовать результаты запроса, возвращаемые asyncpg."""
    return dict(value)


@convert.register(Decimal)
def convert_decimal(value: Decimal):
    """Конвертим Decimal."""
    return float(value)


# Переопределяем функцию конвертации
dumps = partial(json.dumps, default=convert, ensure_ascii=False)


class JsonPayload(BaseJsonPayload):
    """Заменяет функцию сериализации на более "умную" (
        умеющую упаковывать в JSON объекты asyncpg.Record и другие сущности
    ).
    """

    def __init__(
        self,
        value,
        encoding="utf-8",
        content_type="application/json",
        dumps=dumps,
        *args,
        **kwargs,
    ):
        super().__init__(value, encoding, content_type, dumps, *args, **kwargs)


class AsyncGenJSONListPayload(Payload):
    """Итерируется по объектам AsyncIterable, частями сериализует данные из них
    в JSON и отправляет клиенту.
    """

    def __init__(
        self,
        value,
        encoding: str = "utf-8",
        content_type: str = "application/json",
        root_object: str = "data",
        *args,
        **kwargs,
    ):
        self.root_object = root_object
        super().__init__(
            value, content_type=content_type, encoding=encoding, *args, **kwargs
        )

    async def write(self, writer):
        # Начало объекта
        await writer.write(('{"%s":[' % self.root_object).encode(self._encoding))

        first = True
        async for row in self._value:
            # Перед первой строчкой запятая не нужна
            first = False if first else await writer.write(b",")

            await writer.write(dumps(row).encode(self._encoding))

        # Конец объекта
        await writer.write(b"]}")


__all__ = ("JsonPayload", "AsyncGenJSONListPayload")
