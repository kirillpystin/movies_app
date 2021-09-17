from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema, form_schema

from messengerApp.messenger.api.handlers.actors import ActorsActions
from messengerApp.messenger.schemas.actor import ActorSchema, LoadActor

actor_router = web.RouteTableDef()


@actor_router.post("/actors/load")
@docs(summary="Загрузить актеров")
@form_schema(LoadActor())
async def load_actors(file_scv):
    """Извекечение записи об актере.
    Args:
        films_csv(str): Файл с актерами
    """
    return await ActorsActions.load_actors(file_scv)


@actor_router.get("/actors/{record_id}")
@docs(summary="Извлечь актера")
async def get_actor(record_id):
    """Извекечение записи об актере.
    Args:
        record_id(str): id записи
    """
    return await ActorsActions.get_record(record_id)


@actor_router.post("/actors")
@docs(summary="Добавить актера")
@request_schema(ActorSchema())
@response_schema(ActorSchema())
async def create_actor(**kwargs):
    """Создать актера."""
    return await ActorsActions.create(**kwargs)


@actor_router.get("/actors_list/{page_num}")
@docs(summary="Получить список актеров")
@response_schema(ActorSchema())
async def get_actors_list(page_num):
    """Получить список актеров."""
    return await ActorsActions.get_list(page_num)


@actor_router.delete("/actors/{record_id}")
@docs(summary="Удалить актера")
@response_schema(ActorSchema())
async def delete_actor(record_id):
    """Удалить актера."""
    return await ActorsActions.delete(record_id)
