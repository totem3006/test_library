# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from test_library import app
from .models import AuthorModel, BookModel, M2M

@app.route('/')
def index():
    return "Hello, World!"
