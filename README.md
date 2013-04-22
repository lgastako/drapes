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

And let's see how it works without drapes:

    >>> db.do("""INSERT INTO demo_users (username, encrypted_password,
    ...                                  birth_date)
    ...          VALUES ('john', 'drowssap', '07/22/1975')
    ...       """)
    >>> user = db.item("SELECT * FROM demo_users")

    >>> user
    Record(username=u'john', encrypted_password=u'drowssap', birth_date=datetime.date(1975, 7, 22))

    >>> user.username
    u'john'

    >>> user.birth_date
    datetime.date(1975, 7, 22)

    >>> user.is_of_drinking_age()
    Traceback (most recent call last):
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/doctest.py", line 1254, in __run
        compileflags, 1) in test.globs
      File "<doctest README.md[9]>", line 1, in <module>
        user.is_of_drinking_age()
    AttributeError: 'Record' object has no attribute 'is_of_drinking_age'

Ok... that last one didn't work because of course there's no
'is_of_drinking_age' column in the users table. And nor should there be,
because that boolean can be derived instantenously from the birth_date field.

Let's create our first drape to do that:

    >>> from datetime import datetime as dt
    >>> import drapes
    
    >>> class User(drapes.Drape):
    ...     def is_of_drinking_age(self):
    ...         return dt.combine(self.birth_date, dt.time()) < (dt.now() - dt.timedelta(years=21))

And try again, but this time, we'll manually drape our User Drape over the user
record that is returned from the database:

    >>> user = User(db.item("SELECT * FROM demo_users"))

And now when we try our 'is_of_drinking_age' method, of course it works:

    >>> user.is_of_drinking_age()
    True

In addition we could've used the shortcut that all of the db.* functions
are available on any Drape to short the above load call to:

    >>> user = User.item("SELECT * FROM demo_users")

Drapes are stackable, so if we have another Drape, like so:

    >>> class PWChecker(drapes.Drape):
    ...     def authenticates(self, pw):
    ...         return pw == self.encrypted_password[::-1]

Then we can get a user that has both helper functions:

    >>> user = User(PWChecker(db.item("SELECT * FROM demo_users")))
    >>> user.is_of_drinking_age()
    True
    >>> user.authenticates("foo")
    True


