from sqlalchemy.orm import mapper

from movie_app.db.schema import films_table


class Film(object):
    def __init__(self, title, rating, genre):
        self.title = title
        self.rating = rating
        self.genre = genre


mapper(Film, films_table)
