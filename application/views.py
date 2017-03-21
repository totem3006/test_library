# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from application import app
from application.models import AuthorModel, BookModel, M2M

from flask.views import MethodView

@app.route('/')
def index():
    return "Hello, World!"


class AuthorAPI(MethodView):
    def get(self, author_id):
        return str(author_id)


author_api_view = AuthorAPI.as_view(b'authors')
app.add_url_rule(
    '/authors/new/',
    view_func=author_api_view,
    methods=['POST',]
)
app.add_url_rule(
    '/authors/<int:author_id>/',
    view_func=author_api_view,
    methods=['GET', 'PUT', 'DELETE']
)
