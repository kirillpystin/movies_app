"""Модуль тестирования API фильмов."""
import logging
from http import HTTPStatus

import aiohttp
import pytest

from tests.conftest import *

log = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_not_found(
    api_client,
    expected_status=HTTPStatus.NOT_FOUND,
):
    """Проверка невалидного запроса."""
    response = await api_client.get("/invalid_request")
    assert response.status == expected_status.value
