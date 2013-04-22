from contextlib import contextmanager

import db as db_


class Drape(object):

    def __init__(self, row):
        self._row = row


class Draper(object):

    def __init__(self, db=None, *mixins):
        self._mixins = mixins
        self.db = db or db_

    def _wrap(self, row):
        # TODO: Create class return it here etc
        return row

    def item(self, *args, **kwargs):
        return self._wrap(self.db.item(*args, **kwargs))

    def items(self, *args, **kwargs):
        return map(self._wrap, self.db.items(*args, **kwargs))

    def first(self, *args, **kwargs):
        x = self.db.first(*args, **kwargs)
        if x:
            return self._wrap(x)

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
    return Draper(*mixins)
