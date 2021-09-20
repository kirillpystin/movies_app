from sqlalchemy import Column
from sqlalchemy import (ForeignKey, Integer, MetaData,
                        String, Table)
from sqlalchemy.orm import registry

mapper_registry = registry()


# SQLAlchemy рекомендует использовать единый формат для генерации названий для
# индексов и внешних ключей.
# https://docs.sqlalchemy.org/en/13/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

films_table = Table(
    "films",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(80)),
    Column("rating", String(80)),
    Column("genre", String(80)),
)

actor_table = Table(
    "actors",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(80)),
)

actors_to_films = Table(
    "actors_2_films",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("actors_id", ForeignKey("actors.id")),
    Column("film_id", ForeignKey("films.id")),
)
