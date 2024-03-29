from contextlib import contextmanager

import db as db_


class Drape(object):

    def __init__(self, row):
        self._row = row
        self._fields = row._fields
        for field in row._fields:
            print "absorbing field: ", field
            setattr(self, field, getattr(row, field))


class Draper(object):

    def __init__(self, name, db=None, *mixins):
        import ipdb; ipdb.set_trace()
        self._mixins = mixins

    def item(self, *args, **kwargs):
        row = self.db.item(*args, **kwargs)
        return self._drape(row)

    def items(self, *args, **kwargs):
        return map(self._drape, self.db.items(*args, **kwargs))

    def first(self, *args, **kwargs):
        x = self.db.first(*args, **kwargs)
        if x:
            return self._drape(x)

    def count(self, *args, **kwargs):
        return self.db.count(*args, **kwargs)

    def do(self, *args, **kwargs):
        self.db.do(*args, **kwargs)

    @contextmanager
    def tx(self, *args, **kwargs):
        with self.db.tx(*args, **kwargs) as tx:
            yield tx

    @contextmanager
    def txc(self, *args, **kwargs):
        with self.db.txc(*args, **kwargs) as (conn, cursor):
            yield conn, cursor


def drape(name, db=None, *mixins):
    # bind to db
    bases = (Drape,) + mixins
    return type(name, bases, {})
