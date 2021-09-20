"""Модуль, хранящий JSON схемы"""
from marshmallow import Schema
from marshmallow.fields import Field, Int, Str


class LoadActor(Schema):
    file_scv = Field(
        description="Файл для загрузки.", required=True, location="form", type="file"
    )


class ActorSchema(Schema):
    id = Int(dump_only=True)
    name = Str()
