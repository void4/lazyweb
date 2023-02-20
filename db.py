import dataset
from flask import g

from app import *

"""
If it doesn't exist yet, Dataset will create a new file, database.db in this directory
Together with the database.db-shm and database.db-wal files
which are created on reads and writes (do not delete these!), it makes up the database
Open database.db with DB Browser for SQLite to inspect its contents
You can copy these three files somewhere to make a backup of your database
"""

DATABASE = "sqlite:///database.db?check_same_thread=False"

def get_table():
	"""can be called by any function to get access to the database table called 'mytable'"""

	db = getattr(g, "_database", None)

	if db is None:
		db = g._database = dataset.connect(DATABASE)

	return db["mytable"]

"""
We are using the database here to store some previous calculation results, but it could be anything!
some data you collected yourself, user generated content, user accounts...

Just create a new get_<tablename> function for each new table and use them in your new functions
"""

def set_cache(input, output):
	"""creates a new row in the database. dataset will insert columns automatically if they don't exist yet
	the same goes for the table and the database file"""

	table = get_table()

	row = {
		"input": input,
		"output": output
	}

	table.insert(row)

def get_cache(input):
	"""will return None if no row with that input"""

	table = get_table()

	result = table.find_one(input=input)

	if result is None:
		return None

	return result["output"]

"""
Utility to execute requests interactively

$ python
>>> from db import *
>>> with_context(set_cache, 2, 4)
>>> with_context(get_cache, 2)
4.0
"""
def with_context(f, *args, **kwargs):
    with app.app_context():
        return f(*args, **kwargs)
