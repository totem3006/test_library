# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from application import app
from application.models import AuthorModel, BookModel, M2M

@app.route('/')
def index():
    return "Hello, World!"
