from random import shuffle

from flask import render_template, request, jsonify

from app import *
from db import *

@app.route("/")
def r_index():
    return render_template("index.html", somedata="hello", somelistdata=[1,2,3,4,5])

@app.route("/newlist", methods=["POST"])
def r_newlist():
    l = [1,2,3,4,5]

    shuffle(l)

    return jsonify({"somelistdata": l})

@app.route("/square", methods=["POST"])
def r_square():
    """squares a number, checks the database first if the number was already computed,
    if so, it returns the cached result,
    if not, it adds the number and its result to the database
    before sending it back to the user"""

    number = float(request.json["number"])

    cached = get_cache(number)
    if cached is not None:
        print("cached!")
        number_squared = cached
    else:
        number_squared = number**2
        set_cache(number, number_squared)

    return jsonify({"someresult": number_squared})

app.run("localhost", 1337, debug=True)
