import db


class Drape(object):

    def __init__(self, wrapped):
        self._wrapped = wrapped
        self._fields = wrapped._fields
        for field in self._fields:
            setattr(self, field, getattr(self._wrapped, field))

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    @classmethod
    def item(cls, *args, **kwargs):
        row = db.item(*args, **kwargs)
        return cls(row)

    @classmethod
    def items(cls, *args, **kwargs):
        rows = db.items(*args, **kwargs)
        return map(cls, rows)

