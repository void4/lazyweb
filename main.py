from flask import render_template, request, jsonify

from app import *
from db import *

@app.route("/")
def r_index():
    return render_template("index.html", somestaticdata="hello")

@app.route("/square", methods=["POST"])
def r_square():
    number = float(request.json["number"])


    cached = get_cache(number)
    if cached is not None:
        print("cached!")
        return jsonify(cached)

    number_squared = number**2
    set_cache(number, number_squared)

    return jsonify(number_squared)

app.run("localhost", 1337, debug=True)
