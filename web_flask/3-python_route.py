#!/usr/bin/python3
"""A script that starts a Flask web application """

from flask import Flask

app = Flask(__name__)

# Disable strict slashes for the entire app
app.url_map.strict_slashes = False


@app.route('/')
def display():
    """ displays `Hello HBNB!` """
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """ displays `HBNB` """
    return "HBNB"


@app.route('/c/<text>')
def c(text):
    """ displays <text> replacing `_` with ` ` """
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route('/python')
@app.route('/python/<text>')
def python(text="is cool"):
    """ displays <text> replacing `_` with ` ` """
    text = text.replace("_", " ")
    return "Python {}".format(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
