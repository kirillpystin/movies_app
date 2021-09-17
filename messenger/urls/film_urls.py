from aiohttp import web
from aiohttp.web_request import Request
from aiohttp_apispec import docs, request_schema, response_schema

from messenger.api.handlers.films import FilmsActions
from messenger.schemas.film import FilmSchema

film_router = web.RouteTableDef()


@film_router.post("/load_films")
async def load_films(films_csv):
    """Проверить исследование алгоритма.
    Args:
        films_csv(Request): Файл с фильмами

    Returns:
        Response: ответ с статусом алгоритма
    """
    return await FilmsActions.load_films(films_csv)


@film_router.get("/get_film/{record_id}")
@docs(summary="Извлечь фильм")
async def get_film(record_id):
    """Проверить исследование алгоритма.
    Args:
        record_id(str): идентификатор фильма

    Returns:
        Response: ответ с статусом алгоритма
    """
    return await FilmsActions.get_record(record_id)


@film_router.post("/")
@docs(summary="Добавить фильм")
@request_schema(FilmSchema())
@response_schema(FilmSchema())
async def create_film(**kwargs):
    """Добавить фильм."""
    return await FilmsActions.create(**kwargs)


@film_router.get("/films_list/{page_num}")
@docs(summary="Получить список фильмов")
@response_schema(FilmSchema())
async def get_films(page_num):
    """Получить фильмы."""
    return await FilmsActions.get_list(page_num)


@film_router.delete("/films/{film_id}")
@docs(summary="Удалить фильм")
@response_schema(FilmSchema())
async def delete_films(film_id):
    """Удалить фильм."""
    return await FilmsActions.delete(film_id)
