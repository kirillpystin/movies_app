import pytest
from tests.factories.film import FilmFactory
import marshmallow

from messengerApp.messenger.schemas.film import FilmSchema


@pytest.mark.asyncio
async def test_schema_film():
    film = FilmFactory()
    data = FilmSchema().dump(film)

    assert len(data.keys()) == 3
    assert data['rating']
    assert data['jenre']
    assert data['title']



