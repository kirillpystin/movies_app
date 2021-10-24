"""Модуль, отвечающий за маршрутизацию фильмов."""
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Response
from aiohttp.web_request import Request
from aiohttp_apispec import docs, form_schema, request_schema, response_schema

from app.api.handlers.films import FilmsActions
from app.schemas.actor import LoadActor
from app.schemas.film import FilmSchema

film_router = web.RouteTableDef()


@film_router.post("/films/load")
@docs(summary="Загрузить фильмы")
@form_schema(LoadActor())
async def load_films(file_scv):
    """Загрузка фильмов.

    Args:
        file_scv(Request): Файл с фильмами.

    Returns:
        Response: ответ с статусом.
    """
    await FilmsActions.load_films(file_scv)
    return Response(status=HTTPStatus.OK)


@film_router.post("/films/load_films_with_actors/")
@docs(summary="Загрузить фильмы и актеров")
@form_schema(LoadActor())
async def load_films_with_actors(file_scv):
    """Загрузка фильмов и актеров.

    Args:
        file_scv(Request): Файл с фильмами

    Returns:
        Response: ответ с статусом
    """
    await FilmsActions.load_films_and_actors(file_scv)
    return Response(status=HTTPStatus.OK)


@film_router.get("/films/{record_id}")
@docs(summary="Извлечь фильм")
async def get_film(record_id):
    """Извлечь фильм.
    Args:
        record_id(str): идентификатор фильма

    Returns:
        dict: Запись
    """
    return await FilmsActions.get_record(record_id)


@film_router.post("/films")
@docs(summary="Добавить фильм")
@request_schema(FilmSchema())
async def create_film(**kwargs):
    """Добавить фильм."""
    await FilmsActions.create(**kwargs)
    return Response(status=HTTPStatus.CREATED)


@film_router.get("/films")
@docs(summary="Получить список фильмов")
@response_schema(FilmSchema())
async def get_films(**kwargs):
    """Получить фильмы."""
    return await FilmsActions.get_list(kwargs.get("page", 0))


@film_router.delete("/films/{film_id}")
@docs(summary="Удалить фильм")
@response_schema(FilmSchema())
async def delete_film(film_id):
    """Удалить фильм."""
    await FilmsActions.delete(film_id)
    return Response(status=HTTPStatus.OK)


@film_router.put("/films")
@docs(summary="Обновить фильм")
@request_schema(FilmSchema())
@response_schema(FilmSchema())
async def update_film(**kwargs):
    """Обновить поля фидльма."""
    await FilmsActions.update(**kwargs)
    return Response(status=HTTPStatus.OK)
