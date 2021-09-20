"""Модуль тестирования API фильмов."""
import logging
from http import HTTPStatus

import aiohttp
import pytest

from tests.conftest import *

log = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_sending_file(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Проверка валидного запроса на создание записей.

    Отправляем запрос с тестовыми данными и проверяем создание
    всех нужных файлов и записей в БД.
    """

    form = aiohttp.FormData()

    form.add_field("file_scv", open("tests/fixtures/imdb_1000.csv", "rb"))
    response = await api_client.post("/films/load", data=form)
    assert response.status == expected_status.value


@pytest.mark.asyncio
async def test_get_films(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Тест извлечения записи"""

    response = await api_client.get(
        "/films/10",
    )
    response_json = await response.json()

    assert response.status == expected_status.value
    # Проверяем наличие ключей
    assert response_json["genre"]
    assert response_json["title"]
    assert response_json["rating"]


@pytest.mark.asyncio
async def test_get_films_list(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Тест пагинации."""

    response = await api_client.get(
        "/films",
    )
    response_json = await response.json()

    assert response.status == expected_status.value
    assert len(response_json) == 100
    assert response_json[0]["id"] == 1
    assert response_json[-1]["id"] == 100
    # Проверяем наличие ключей

    response = await api_client.get(
        "/films?page=1",
    )
    response_json = await response.json()
    assert response_json[0]["id"] == 101
    assert response_json[-1]["id"] == 200


@pytest.mark.asyncio
async def test_delete_film(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Тест удаления."""

    # Проверяем наличие
    response = await api_client.get(
        "/films/10",
    )
    response_json = await response.json()

    assert response_json

    # Проверяем удаление
    response = await api_client.delete(
        "/films/10",
    )
    assert response.status == expected_status.value

    response = await api_client.get(
        "/films/10",
    )
    response_json = await response.json()
    assert not response_json


@pytest.mark.asyncio
async def test_create_film(
    api_client,
    expected_status=HTTPStatus.CREATED,
):
    """Тест создания фильма."""
    response = await api_client.post(
        "/films",
        data={
            "title": "Иван Васильевич меняет профессию",
            "genre": "Комедия",
            "rating": "10",
        },
    )

    assert response.status == expected_status.value


@pytest.mark.asyncio
async def test_update_film(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Обновление фильма"""
    film_id = 12
    response = await api_client.get(
        f"/films/{film_id}",
    )
    response_json = await response.json()
    initial_name = response_json.get("name")

    new_name = "Allan Delon"
    await api_client.put(f"/films", data={"id": film_id, "title": new_name})

    response = await api_client.get(
        f"/films/{film_id}",
    )
    response_json = await response.json()

    updated_name = response_json.get("title")

    assert initial_name != updated_name
    assert updated_name == new_name
    assert response.status == expected_status.value
