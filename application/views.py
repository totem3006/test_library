# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import time
import config

from flask import request
from flask.views import MethodView

from application import app
from application import cache
from application.models import AuthorModel
from application.models import BookModel
from application.models import db_session
from application.forms import AuthorCreateForm
from application.forms import AuthorUpdateForm
from application.forms import BookCreateForm
from application.forms import BookUpdateForm


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
        try:
            request_data = json.loads(request.data)
        except ValueError:
            return 'Request is not valid JSON', 400

        if set(request_data.keys()) - {'description', 'name'}:
            # There is a parameter differ then {'description', 'name'}
            error_msg = 'Unexpected params: %s' % \
                ', '.join(set(request_data.keys()) - {'description', 'name'})
            return error_msg, 400

        form = AuthorUpdateForm.from_json(request_data)

        if not form.validate():
            return 'Invalid request data', 400

        author = AuthorModel.query.filter_by(id=author_id).first()

        if author is None:
            error_msg = 'User %d doest\'t exist' % int(author_id)
            return error_msg, 404

        if 'name' in request_data:
            author.name = request_data['name']

        if 'description' in request_data:
            author.description = request_data['description']

        db_session.add(author)

        db_session.commit()
        return 'Ok', 200

    def delete(self, author_id):
        author = AuthorModel.query.filter_by(id=author_id)

        if author.first() is None:
            error_msg = 'User %d doest\'t exist' % int(author_id)
            return error_msg, 404

        author.delete()

        db_session.commit()

        return 'Ok', 200

    def post(self):
        try:
            request_data = json.loads(request.data)
        except ValueError:
            return 'Invalid request body', 400

        form = AuthorCreateForm.from_json(request_data)

        if not form.validate():
            return 'Invalid request', 400

        author = AuthorModel(name=request_data['name'], description=request_data['description'])
        db_session.add(author)
        db_session.commit()

        return str(author.id), 200


class BookAPI(MethodView):

    def get(self, book_id):
        book = BookModel.query.filter_by(id=book_id).first()

        if book is None:
            return 'Book not found', 404

        return book.to_JSON(), 200

    def delete(self, book_id):
        book = BookModel.query.filter_by(id=book_id)

        if book.first() is None:
            return 'Book not found', 404

        book.delete()

        db_session.commit()

        return 'Ok', 200

    def post(self):
        try:
            request_data = json.loads(request.data)
        except ValueError:
            return 'Request body is not a valid JSON', 400

        if len(request_data) != 3:
            return 'Invalid request data', 400

        form = BookCreateForm.from_json(request_data)

        if not form.validate():
            return 'Invalid request data', 400

        book = BookModel(name=request_data['name'], description=request_data['description'])
        db_session.add(book)

        for author_id in request_data['authors']:
            author = AuthorModel.query.filter_by(id=author_id).first()

            if author is None:
                msg = 'Author %d doesn\'t exist' % author_id
                db_session.rollback()
                return msg, 404
            book.authors.append(author)

        db_session.commit()

        return str(book.id), 200

    def put(self, book_id):
        try:
            request_data = json.loads(request.data)
        except ValueError:
            return 'Request body is not a valid JSON', 400

        if set(request_data.keys()) - {'name', 'description', 'authors'}:
            return 'Invalid request data', 400

        form = BookUpdateForm.from_json(request_data)

        if not form.validate():
            return 'Invalid request data', 400

        new_authors = []
        if 'authors' in request_data:
            for author_id in request_data['authors']:
                new_author = AuthorModel.query.filter_by(id=author_id).first()
                if new_author is None:
                    msg = 'Author with id = %d is noe existing' % author_id
                    return msg, 404

                new_authors.append(new_author)

        book = BookModel.query.filter_by(id=book_id).first()

        if book is None:
            msg = 'Book with id=%d doesn\'t exist' % book_id
            return msg, 404

        db_session.add(book)

        if 'name' in request_data:
            book.name = request_data['name']

        if 'description' in request_data:
            book.description = request_data['description']

        if 'authors' in request_data:
            book.authors = new_authors

        db_session.commit()

        return 'Ok', 200


@app.route('/library/', methods=['GET', ])
@app.route('/library/<int:page>/', methods=['GET', ])
def library_api(page=1):
    response = BookModel.query.order_by('id')\
                              .offset((page - 1) * config.LIBRARY_PAGE_SIZE)\
                              .limit(config.LIBRARY_PAGE_SIZE)

    if not response.count():
        msg = 'Books not found for page %d and page size %d' % (page, config.LIBRARY_PAGE_SIZE)
        return msg, 404

    return json.dumps(
        [it.to_dict() for it in response],
        ensure_ascii=False
    ).encode('utf8')


# this method contains heave calculation
@cache.cached(timeout=60, key_prefix='calculate_statictic')
def calculate_statictic():
    books_count = BookModel.query.count()
    authors_count = AuthorModel.query.count()

    time.sleep(2.0)

    return {'books': books_count, 'authors': authors_count, }


@app.route('/statistics/', methods=['GET', ])
def statistic_api():
    stats = calculate_statictic()

    return json.dumps(stats)

author_api_view = AuthorAPI.as_view(b'authors')
app.add_url_rule(
    '/authors/new/',
    view_func=author_api_view,
    methods=['POST', ]
)
app.add_url_rule(
    '/authors/<int:author_id>/',
    view_func=author_api_view,
    methods=['GET', 'PUT', 'DELETE']
)

book_api_view = BookAPI.as_view(b'book')
app.add_url_rule(
    '/book/<int:book_id>/',
    view_func=book_api_view,
    methods=['GET', 'PUT', 'DELETE']
)
app.add_url_rule(
    '/book/new/',
    view_func=book_api_view,
    methods=['POST']
)
