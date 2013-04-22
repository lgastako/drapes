drapes
======

A lightweight ORM for the 'db' library.

The design of drapes is driven by experiencing the good, the bad, and the ugly
of ORMs.  I want to be as close to the data as possible, and I know this may
sound strange, but I actually like writing SQL.  But I also recognize that
there are some reoccuring patterns that are tedious to manage without something
like an ORM, hence... drapes.

The name comes from the fact the the objects that are created by the ORM behave
as if they are "draped over" the raw records that come back from the database.

In fact, at any given moment, they may or may not be implemented as some sort
of proxy object (as I write this, they are not, they pull the elements out
of the database records and inject them into themself).


Basic Usage
-----------

First, let's get a basic database going:

    >>> import db
    >>> db.drivers.psycopg2x.register("user=demo dbname=demo host=localhost password=demo port=6432")
    ...                                                     # doctest: +ELLIPSIS
    <db.Database object at ...>
    >>> db.do("DROP TABLE IF EXISTS demo_users")
    >>> db.do("""CREATE TABLE demo_users (
    ...              username TEXT PRIMARY KEY,
    ...              encrypted_password TEXT NOT NULL,
    ...              birth_date DATE NOT NULL
    ...          ); 
    ...       """)

And test see how it works without drapes:

    >>> db.do("""INSERT INTO demo_users (username, encrypted_password,
    ...                                  birth_date)
    ...          VALUES ('john', 'drowssap', '07/22/1975')
    ...       """)
    >>> db.item("SELECT * FROM demo_users")
    Record(username=u'john', encrypted_password=u'drowssap', birth_date=datetime.date(1975, 7, 22))


