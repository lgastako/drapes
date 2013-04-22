import db as db_


class Drape(object):

    def __init__(self, wrapped, db=None):
        self._wrapped = wrapped
        self._fields = wrapped._fields
        for field in self._fields:
            setattr(self, field, getattr(self._wrapped, field))
        self._db = db or db_

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def compose(self, *others):
        return DrapeStack([self.__class__] + list(others))

    @classmethod
    def item(self, *args, **kwargs):
        return self.__class__(self._db.item(*args, **kwargs))

    def items(self, *args, **kwargs):
        return map(self.__class__, self._db.items(*args, **kwargs))

    def first(self, *args, **kwargs):
        return self.__class__(self._db.first(*args, **kwargs))

    def count(self, *args, **kwargs):
        return self._db.count(*args, **kwargs)

    def do(self, *args, **kwargs):
        self._db.do(*args, **kwargs)


class DrapeStack(object):

    def __init__(self, drapes):
        self.drapes = drapes
        self._db = self.drapes[0]._db

    def __call__(self, row):
        return self._wrap(row)

    def _wrap(self, row):
        for drape in self.drapes[::-1]:
            row = drape(row)
        return row

    def item(self, *args, **kwargs):
        row = self._db.item(*args, **kwargs)
        return self._wrap(row)

    def items(self, *args, **kwargs):
        rows = self._db.items(*args, **kwargs)
        return map(self._wrap, rows)

    def first(self, *args, **kwargs):
        row = self._db.first(*args, **kwargs)
        return self._wrap(row)

    def count(self, *args, **kwargs):
        return self._db.count(*args, **kwargs)

    def do(self, *args, **kwargs):
        return self._db.do(*args, **kwargs)

