#!/usr/bin/python3
"""
a script that starts a Flask web application.
web application must be listening on 0.0.0.0, port 5000
"""

from flask import Flask

app = Flask("__name__")


@app.route('/', strict_slashes=False)
def home():
    """display Hello HBNB!"""
    return ("Hello HBNB!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
