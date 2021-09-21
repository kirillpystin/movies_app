from sqlalchemy.orm import registry, relationship

from movie_app.db.schema import *

from .actor import Actor
from .film import Film

mapper_registry = registry()

mapper_registry.map_imperatively(
    Actor,
    actor_table,
    properties={
        "films": relationship(
            Film, secondary=actors_to_films, backref="films", lazy="subquery"
        )
    },
)

mapper_registry.map_imperatively(
    Film,
    films_table,
    properties={
        "actors": relationship(
            Actor, secondary=actors_to_films, backref="actors", lazy="subquery"
        )
    },
)
