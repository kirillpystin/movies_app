from messenger.models import Film
from messenger.schemas.film import FilmSchema

from .base import Core


class FilmsActions(Core):
    """Действия над фильмами."""
    model = Film
    schema = FilmSchema()

    @classmethod
    async def load_films(cls, films_csv):
        """Загрузка фильмов из csv в БД.

        Args:
            films_csv: Файл с фильмами.
        """
        await cls.add_records(cls.get_films_data(cls.read_csv(films_csv)))

    @staticmethod
    def get_films_data(films):
        """Извлечение информации о фильмах.

        Args:
            films: список фильмов

        Returns:
            list: Список фильмов
        """
        return [
            Film(
                **{
                    "title": f["title"],
                    "genre": f["genre"],
                    "rating": f["star_rating"],
                }
            )
            for f in films
        ]

    @classmethod
    async def load_films_and_actors(cls, films_csv):
        """Загрузка фильмов из csv в БД.

        Args:
            films_csv: Файл с фильмами.
        """
        await cls.add_records(cls.get_films_data(cls.read_csv(films_csv)))

