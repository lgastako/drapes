import db
import sqlite3

from drapes import drape


class TestSomething:
    
    def setup_method(self, method):
        db.drivers.clear()
        db.drivers.sqlite3x.register(":memory:")
        db.do("CREATE TABLE tests (name TEXT)")
        db.do("INSERT INTO tests (name) VALUES ('foo')")

    def test_something(self):
        Null = drape("Null") 
        sql = "SELECT COUNT(*) AS n FROM tests"
        assert Null.item(sql).n == db.item(sql).n == 1
