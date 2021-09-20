"""Модуль тестирования API для актеров."""
import logging
from http import HTTPStatus

import aiohttp
import pytest

from movie_app.api.handlers import *
from movie_app.models import *
from tests.conftest import *

log = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_sending_file(
    api_client,
    expected_status=HTTPStatus.CREATED,
):
    """Проверка создания записей из файла."""
    form = aiohttp.FormData()
    form.add_field("file_scv", open("tests/fixtures/imdb_1000.csv", "rb"))
    response = await api_client.post("/actors/load", data=form)

    assert response.status == expected_status.value


@pytest.mark.asyncio
async def test_get_actor(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Тест извлечения записи."""

    response = await api_client.get(
        "/actors/10",
    )
    response_json = await response.json()

    assert response.status == expected_status.value
    # Проверяем наличие ключей
    assert response_json["id"]
    assert response_json["name"]


@pytest.mark.asyncio
async def test_create_actor(
    api_client,
    expected_status=HTTPStatus.CREATED,
):
    """Тест создания записи."""
    response = await api_client.post("/actors", data={"name": "Джеки чан"})
    assert response.status == expected_status.value


@pytest.mark.asyncio
async def test_get_films_list(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Тест пагинации."""

    response = await api_client.get(
        "/actors",
    )
    response_json = await response.json()

    assert response.status == expected_status.value
    assert len(response_json) == 100
    assert response_json[0]["id"] == 1
    assert response_json[-1]["id"] == 100
    # Проверяем наличие ключей

    response = await api_client.get(
        "/actors?page=1",
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
        "/actors/10",
    )
    response_json = await response.json()

    assert response_json

    # Проверяем удаление
    response = await api_client.delete(
        "/actors/10",
    )
    assert response.status == expected_status.value

    response = await api_client.get(
        "/actors/10",
    )
    response_json = await response.json()
    assert not response_json


@pytest.mark.asyncio
async def test_update_actor(
    api_client,
    expected_status=HTTPStatus.OK,
):
    """Обновление актера"""
    actor_id = 12
    response = await api_client.get(
        f"/actors/{actor_id}",
    )
    response_json = await response.json()
    initial_name = response_json.get("name")

    new_name = "Allan Delon"
    await api_client.put(f"/actors", data={"id": actor_id, "name": new_name})

    response = await api_client.get(
        f"/actors/{actor_id}",
    )
    response_json = await response.json()

    updated_name = response_json.get("name")

    assert initial_name != updated_name
    assert updated_name == new_name
    assert response.status == expected_status.value
