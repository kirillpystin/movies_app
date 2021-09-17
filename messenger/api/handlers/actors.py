from messenger.models import Actor
from messenger.schemas.actor import ActorSchema
import ast

from .base import Core


class ActorsActions(Core):
    """Действия над актерами."""

    model = Actor
    schema = ActorSchema()

    @classmethod
    async def load_actors(cls, films_csv):
        """Загрузка фильмов из csv в БД.

        Args:
            films_csv: Файл с фильмами.
        """
        await cls.add_records(cls.get_actors_data(cls.read_csv(films_csv)))

    @staticmethod
    def get_actors_data(films):
        """Извлечение информации об актерах.

        Args:
            films: список фильмов

        Returns:
            list: Список фильмов
        """
        actors_list_films = [ast.literal_eval((i['actors_list'])) for i in films]
        actors_list = tuple(set([actor_name for f in actors_list_films for actor_name in f]))

        return [Actor(**{"name": actor_name}) for actor_name in actors_list]
