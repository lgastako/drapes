import db as db_


class Drape(object):

    def __init__(self, row):
        self._row = row


class Draper(object):

    def __init__(self, db=None, *mixins):
        self._mixins = mixins
        self._db = db or db_

    def _wrap(self, row):
        # TODO: Create class return it here etc
        return row

    def item(self, *args, **kwargs):
        return self._wrap(self._db.item(*args, **kwargs))

    def items(self, *args, **kwargs):
        return map(self._wrap, self._db.items(*args, **kwargs))

    def first(self, *args, **kwargs):
        x = self._db.first(*args, **kwargs)
        if x:
            return self._wrap(x)

    def count(self, *args, **kwargs):
        return self._db.count(*args, **kwargs)


def drape(name, db=None, *mixins):
    return Draper(*mixins)

