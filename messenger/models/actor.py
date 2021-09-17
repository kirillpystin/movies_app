from sqlalchemy.orm import mapper

from messenger.db.schema import actor_table


class Actor(object):
    def __init__(self, name):
        self.name = name


mapper(Actor, actor_table)
