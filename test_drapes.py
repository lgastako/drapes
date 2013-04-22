import db
import sqlite3

from drapes import drape


class DBTMixin(object):

    def setup_method(self, method):
        self.Null = drape("Null") 
        self.sql = "SELECT COUNT(*) AS n FROM tests"
        db.drivers.clear()
        db.drivers.sqlite3x.register(":memory:")
        db.do("CREATE TABLE tests (name TEXT)")
        db.do("""CREATE TABLE users (
                    username TEXT,
                    encrypted_pw TEXT,
                    dob DATE
                 )""")
        db.do("INSERT INTO tests (name) VALUES ('foo')")
        db.do("""INSERT INTO users (username, encrypted_pw, dob)
                 VALUES ('john', 'drowssap', '07/22/1975')
              """)


class TestNullPassthroughs(DBTMixin):
    
    def test_item(self):
        self.sql = "SELECT * FROM tests"
        assert self.Null.item(self.sql).name == db.item(self.sql).name == "foo"

    def test_items(self):
        self.sql = "SELECT name FROM tests"
        null_items = self.Null.items(self.sql)
        db_items = db.items(self.sql)
        nn = lambda xs: map(lambda x: x.name, xs)
        assert nn(null_items) == nn(db_items) == ["foo"]

    def test_first(self):
        assert self.Null.first(self.sql).n == db.first(self.sql).n == 1

    def test_count(self):
        assert self.Null.count("tests") == db.count("tests") == 1

    def test_do(self):
        self.Null.do("INSERT INTO tests (name) VALUES ('bar')")
        assert self.Null.count("tests") == 2

    def test_tx(self):
        with self.Null.tx() as tx:
            assert tx.count("tests") == 1
            
    def test_txc(self):
        with self.Null.txc() as (conn, cursor):
            cursor.execute("SELECT COUNT(*) AS n FROM tests")
            assert cursor.fetchone().n == 1


class BouncerMixin(object):

    def is_legal(self):
        #return (dt.datetime.combine(self.birth_date, dt.time())
        #        < dt.datetime.now() - dt.timedelta(days-365 * 21))
        
        birth_dt = dt.datetime.combine(self.birth_date, dt.time())
        now = dt.datetime.now()
        return now - birth_dt >= dt.timedelta(days=365 * 21)


class TestSingleMixin(DBTMixin):

    def test_foo(self):
        User = drape("User", BouncerMixin)
        user = User.item("SELECT * FROM users")
        assert user.is_legal()

