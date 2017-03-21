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
        author = AuthorModel.query.filter_by(id=author_id).first()

        if author is None:
            error_msg = 'User %d doest\'t exist' % int(author_id)
            return error_msg, 404

        return author.to_JSON(), 200


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
