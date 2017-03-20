# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import Flask

import config

app = Flask(config.PROJECT_NAME)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
