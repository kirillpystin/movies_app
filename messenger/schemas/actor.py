"""
Модуль содержит схемы для валидации данных в запросах и ответах.
Схемы валидации запросов используются в бою для валидации данных отправленных
клиентами.
Схемы валидации ответов *ResponseSchema используются только при тестировании,
чтобы убедиться что обработчики возвращают данные в корректном формате.
"""
from marshmallow import Schema, ValidationError, validates, validates_schema
from marshmallow.fields import Date, Dict, Float, Int, List, Nested, Str, Field


class LoadActor(Schema):
    file_scv = Field(
        description="Файл для загрузки.",
        required=True,
        location="form",
        type="file"
    )


class ActorSchema(Schema):
    id = Int(dump_only=True)
    name = Str()
