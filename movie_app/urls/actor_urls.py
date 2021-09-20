"""Модуль с маршрутизацией для актеров."""
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Response
from aiohttp_apispec import docs, form_schema, request_schema, response_schema

from movie_app.api.handlers.actors import ActorsActions
from movie_app.schemas.actor import ActorSchema, LoadActor

actor_router = web.RouteTableDef()


@actor_router.post("/actors/load")
@docs(summary="Загрузить актеров")
@form_schema(LoadActor())
async def load_actors(file_scv):
    """Извекечение записи об актере.

    Args:
        file_scv(str): Файл с актерами.
    Returns:
        Response: Ответ с статусом.
    """
    await ActorsActions.load_actors(file_scv)
    return Response(status=HTTPStatus.CREATED)


@actor_router.get("/actors/{record_id}")
@docs(summary="Извлечь актера")
async def get_actor(record_id):
    """Извекечение записи об актере.
    Args:
        record_id(str): id записи.
    Returns:
        dict: Словарь с записью.
    """
    return await ActorsActions.get_record(record_id)


@actor_router.post("/actors")
@docs(summary="Добавить актера")
@request_schema(ActorSchema())
@response_schema(ActorSchema())
async def create_actor(**kwargs):
    """Создать актера.

    Args:
        kwargs: Параметры для создания записи.
    Returns:
        Response: Ответ с статусом.
    """
    await ActorsActions.create(**kwargs)
    return Response(status=HTTPStatus.CREATED)


@actor_router.get("/actors")
@docs(summary="Получить список актеров")
@response_schema(ActorSchema())
async def get_actors_list(**kwargs):
    """Получить список актеров.

    Args:
        kwargs: параметры пагинации.
    Returns:
        list: Список записей.
    """
    return await ActorsActions.get_list(kwargs.get("page", 0))


@actor_router.delete("/actors/{record_id}")
@docs(summary="Удалить актера")
@response_schema(ActorSchema())
async def delete_actor(record_id):
    """Удалить актера.

    Args:
        record_id(str): id записи.
    Returns:
        Response: Ответ с статусом.
    """
    await ActorsActions.delete(record_id)
    return Response(status=HTTPStatus.OK)


@actor_router.put("/actors")
@docs(summary="Обновить актера")
@request_schema(ActorSchema())
@response_schema(ActorSchema())
async def update_actor(**kwargs):
    """Обновить поля актера.

    Args:
        kwargs(dict): Параметры для обновления.
    Returns:
        Response: Ответ с статусом.
    """
    await ActorsActions.update(**kwargs)
    return Response(status=HTTPStatus.OK)
