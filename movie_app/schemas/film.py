"""Модуль валидации JSON схемы"""
from marshmallow import Schema
from marshmallow.fields import Float, Int, Str


class FilmGetSchema(Schema):
    record_id = Int()


class FilmSchema(Schema):
    id = Int(dump_only=True)
    title = Str()
    rating = Float()
    genre = Str()
