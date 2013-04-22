import db
import sqlite3

from drapes import drape


class TestNull:
    
    def setup_method(self, method):
        self.Null = drape("Null") 
        self.sql = "SELECT COUNT(*) AS n FROM tests"
        db.drivers.clear()
        db.drivers.sqlite3x.register(":memory:")
        db.do("CREATE TABLE tests (name TEXT)")
        db.do("INSERT INTO tests (name) VALUES ('foo')")

    def test_item_passthrough(self):
        self.sql = "SELECT COUNT(*) AS n FROM tests"
        assert self.Null.item(self.sql).n == db.item(self.sql).n == 1

    def test_items_passthrough(self):
        self.sql = "SELECT name FROM tests"
        null_items = self.Null.items(self.sql)
        db_items = db.items(self.sql)
        nn = lambda xs: map(lambda x: x.name, xs)
        assert nn(null_items) == nn(db_items) == ["foo"]

    def test_first_passthrough(self):
        assert self.Null.first(self.sql).n == db.first(self.sql).n == 1

    def test_count_passthrough(self):
        assert self.Null.count("tests") == db.count("tests") == 1
