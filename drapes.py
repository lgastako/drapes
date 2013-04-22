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
    def compose(cls, *others):
        return DrapeStack([cls] + list(others))

    @classmethod
    def item(cls, *args, **kwargs):
        row = db.item(*args, **kwargs)
        return cls(row)

    @classmethod
    def items(cls, *args, **kwargs):
        rows = db.items(*args, **kwargs)
        return map(cls, rows)


class DrapeStack(object):

    def __init__(self, drapes):
        self.drapes = drapes

    def __call__(self, row):
        return self._wrap(row)

    def _wrap(self, row):
        for drape in self.drapes[::-1]:
            row = drape(row)
        return row

    def item(self, *args, **kwargs):
        row = db.item(*args, **kwargs)
        return self._wrap(row)

    def items(self, *args, **kwargs):
        rows = db.items(*args, **kwargs)
        return map(self._wrap, rows)
