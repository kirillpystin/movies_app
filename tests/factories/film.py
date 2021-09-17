import factory

from messenger.models.film import Film
from tests.conftest import async_session
from .async_factory import AsyncFactory
from factory.faker import faker


fake = faker.Faker()
print(async_session)


class FilmFactory(factory.Factory):
    class Meta:
        model = Film

    title = fake.word()
    rating = fake.pyint()
    genre = fake.word()
