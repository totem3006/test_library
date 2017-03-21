# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from flask import request
from flask.views import MethodView

from application import app
from application.models import AuthorModel, BookModel, M2M, db_session

@app.route('/')
def index():
    return "Hello, World!"


class AuthorAPI(MethodView):
    def get(self, author_id):
        author = AuthorModel.query.filter_by(id=author_id).first()

        if author is None:
            error_msg = 'Object %d doest\'t exist' % int(author_id)
            return error_msg, 404

        return author.to_JSON(), 200

    def put(self, author_id):
        request_data = json.loads(request.data)

        author = AuthorModel.query.filter_by(id=author_id).first()

        if author is None:
            error_msg = 'User %d doest\'t exist' % int(author_id)
            return error_msg, 404

        if not request_data:
            return 'Empty request', 400

        if set(request_data.keys()) - {'description', 'name'}:
            # There is a parameter differ then {'description', 'name'}
            error_msg = 'Unexpected params: %s' % \
                ', '.join(set(request_data.keys()) - {'description', 'name'})
            return error_msg, 400

        if 'name' in request_data:
            '''
            Object name is Column('name', String(255)),
            but I cannot catch this exception in SQLite3
            '''
            if request_data['name'] is None:
                return 'name is not nullable', 400
            author.name = request_data['name']

        if 'description' in request_data:
            if request_data['description'] is None:
                return 'description is not nullable', 400
            author.description = request_data['description']


        db_session.add(author)

        db_session.commit()
        return 'Ok', 200

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
