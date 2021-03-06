import ast

from app.db.schema import films_table
from app.models import Film
from app.schemas.film import FilmSchema

from .actors import ActorsActions
from .base import Core


class FilmsActions(Core):
    """Действия над фильмами."""

    model = Film
    schema = FilmSchema()
    table = films_table

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
            films: список фильмов.

        Returns:
            list: Список фильмов.
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
        await cls.add_records(
            await cls.get_films_and_actors_data(cls.read_csv(films_csv))
        )

    @classmethod
    async def get_films_and_actors_data(cls, films):
        """Извлечение информации о фильмах и актерах.

        Args:
            films(list): список фильмов.

        Returns:
            list: Список фильмов.
        """

        actors_dict = {i.name: i for i in await ActorsActions.get_all()}

        films_list = []
        for f in films:
            film = Film(
                **{
                    "title": f["title"],
                    "genre": f["genre"],
                    "rating": f["star_rating"],
                }
            )

            for actor in ast.literal_eval(f["actors_list"]):
                film.actors.append(actors_dict.get(actor))

            films_list.append(film)

        return films_list
