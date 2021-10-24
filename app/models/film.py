"""Модель фильма."""


class Film(object):
    def __init__(self, title, rating, genre):
        self.title = title
        self.rating = rating
        self.genre = genre
