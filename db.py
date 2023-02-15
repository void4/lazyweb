import dataset
from flask import g

from app import *

DATABASE = "sqlite:///database.db?check_same_thread=False"

def get_table():
	"""can be called by any function to get access to the database table called 'mytable'"""

	db = getattr(g, "_database", None)
	if db is None:
		db = g._database = dataset.connect(DATABASE)
	table = db["mytable"]
	return table

def set_cache(input, output):
	"""creates a new row in the database. dataset will insert columns automatically if they don't exist yet, the same goes for the database file"""

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
