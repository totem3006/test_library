# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

import config

from flask import request
from flask.views import MethodView

from application import app
from application.models import AuthorModel, BookModel, db_session


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
            return 'Invalid request body', 400

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

        if not request_data:
            return 'Empty request', 400

        if len(request_data.keys()) != 2 or \
           'name' not in request_data or \
           request_data['name'] is None or \
           'description' not in request_data or \
           request_data['description'] is None:

            error_msg = 'Unexpected params: %s' % \
                ', '.join(set(request_data.keys()) - {'description', 'name'})
            return 'Bad request', 400

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
            return 'Invalid request body', 400

        if not request_data:
            return 'Empty request', 400

        if len(request_data) != 3 or \
                'name' not in request_data or \
                request_data['name'] is None or \
                'description' not in request_data or \
                request_data['description'] is None or \
                'authors' not in request_data or \
                request_data['authors'] is None:
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

        if not request_data or \
                ('name' in request_data and request_data['name'] is None) or \
                ('description' in request_data and request_data['description'] is None) or \
                ('authors' in request_data and request_data['authors'] is None) or \
                (set(request_data.keys()) - {'name', 'description', 'authors'}):
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


@app.route('/library/', methods = ['GET', ])
@app.route('/library/<int:page>/', methods = ['GET', ])
def library_api(page = 1):
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
