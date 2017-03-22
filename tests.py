# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest
import tempfile
import json
import random
import datetime
import timeout_decorator

import config

from application import app
from application import cache
from application.models import db_session
from application.models import AuthorModel
from application.models import BookModel
from application.models import BookAuthorM2M


class AuthorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        AuthorModel.query.delete()
        BookModel.query.delete()
        BookAuthorM2M.query.delete()

    def tearDown(self):
        pass

    def get_nonexisting_id(self, ModelClass):
        try:
            last_item = ModelClass.query.order_by('id')[-1]
            non_existing_id = last_item.id + 1
        except IndexError:
            non_existing_id = 1

        return non_existing_id

    def add_author(self, test_name):
        author = AuthorModel(name=test_name, description=test_name)
        db_session.add(author)
        db_session.commit()

        return author

    def test_000_get_response_200(self):
        author = self.add_author('test_000_get_response_200')

        url = '/authors/{id:d}/'.format(id=author.id)
        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)

    def test_001_get_normal_json_validate(self):
        author = self.add_author('test_001_get_normal_json_validate')

        url = '/authors/{id:d}/'.format(id=author.id)
        response = self.app.get(url, follow_redirects=True)

        json_author = json.loads(response.data, encoding='utf8')

        author_name = json_author['name']
        author_description = json_author['description']

        self.assertEqual(author_name, 'test_001_get_normal_json_validate')
        self.assertEqual(author_description, 'test_001_get_normal_json_validate')

    def test_002_get_non_existing_author(self):
        non_existing_id = self.get_nonexisting_id(AuthorModel)

        url = '/authors/{id:d}/'.format(id=non_existing_id)
        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(404, response.status_code)

    def test_003_put_user_200(self):
        author = self.add_author('test_003_put_user_200')

        url = '/authors/{id:d}/'.format(id=author.id)
        data = {'name': 'newname003', 'description': 'newdescription003'}
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)

    def test_004_put_user_both_fields(self):
        author = self.add_author('test_004_put_user_both_fields')
        author_id = author.id

        url = '/authors/{id:d}/'.format(id=author.id)
        data = {'name': 'newname004', 'description': 'newdescription004'}
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()

        author_name = author.name
        author_description = author.description

        self.assertEqual('newname004', author_name)
        self.assertEqual('newdescription004', author_description)

    def test_005_put_single_field(self):
        author = self.add_author('test_005_put_single_field')
        author_id = author.id

        # update name
        url = '/authors/{id:d}/'.format(id=author.id)
        data = {'name': 'newname005', }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()

        author_name = author.name
        author_description = author.description
        self.assertEqual('newname005', author_name)
        self.assertEqual('test_005_put_single_field', author_description)

        author.name = 'test_005_put_single_field'
        db_session.add(author)
        db_session.commit()

        # update description
        data = {'description': 'newdescription005', }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()
        author_name = author.name
        author_description = author.description
        self.assertEqual('test_005_put_single_field', author_name)
        self.assertEqual('newdescription005', author_description)

    ########################################################
    def test_006_put_bad_requests_400(self):
        author = self.add_author('test_006_put_bad_requests_400')
        author_id = author.id

        url = '/authors/{id:d}/'.format(id=author.id)

        datas = [
            {},
            {'name': 'newname006', 'description': 'newdescription006', 'whoiam': 'lalala'},
            {'name': None, },
            {'description': None, },
        ]

        for data in datas:
            response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

            self.assertEqual(400, response.status_code)
            author = AuthorModel.query.filter_by(id=author_id).first()

            self.assertIsNotNone(author)
            self.assertEqual('test_006_put_bad_requests_400', author.name)
            self.assertEqual('test_006_put_bad_requests_400', author.description)

    def test_009_put_nonexisting_author(self):
        non_existing_id = self.get_nonexisting_id(AuthorModel)

        url = '/authors/{id:d}/'.format(id=non_existing_id)

        data = {'name': 'NewName009', }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(404, response.status_code)

    def test_010_delete_200(self):
        author = self.add_author('test_010_delete_200')

        url = '/authors/{id:d}/'.format(id=author.id)
        response = self.app.delete(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)

    def test_011_delete_successfully(self):
        author = self.add_author('test_011_successfully_delete')
        author_id = author.id

        url = '/authors/{id:d}/'.format(id=author.id)
        response = self.app.delete(url, follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()

        self.assertIsNone(author)

    def test_012_delete_unexising_author(self):
        non_existing_id = self.get_nonexisting_id(AuthorModel)

        url = '/authors/{id:d}/'.format(id=non_existing_id)

        data = {'name': 'NewName009', }
        response = self.app.delete(url, follow_redirects=True)

        self.assertEqual(404, response.status_code)

    def test_013_post_good_params_and_200(self):
        url = '/authors/new/'

        data = {'name': 'test_013_post_good_params_and_200',
                'description': 'test_013_post_good_params_and_200'}
        response = self.app.post(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)

        new_object_id = int(response.data)

        author = AuthorModel.query.filter_by(id=new_object_id).first()
        self.assertIsNotNone(author)

        self.assertEqual('test_013_post_good_params_and_200', author.name)
        self.assertEqual('test_013_post_good_params_and_200', author.description)

    def test_014_post_bad_requests_examples(self):
        url = '/authors/new/'

        datas = [
            {},
            {'name': 'test_013_post_good_params_and_200', },
            {'description': 'test_013_post_good_params_and_200', },
            {'name': None, 'description': 'test_013_post_good_params_and_200', },
            {'name': 'test_013_post_good_params_and_200', 'description': None, },
            {'invalid_param': 'zzzz', 'description': 'test_013_post_good_params_and_200'}
        ]

        for data in datas:
            response = self.app.post(url, data=json.dumps(data), follow_redirects=True)
            self.assertEqual(400, response.status_code)

    def test_015_put_post_not_valid_json(self):
        url = '/authors/new/'

        data = 'It\'s not a json'
        response = self.app.post(url, data=data, follow_redirects=True)
        self.assertEqual(400, response.status_code)

        author = self.add_author('test_015_non_json_for_put_and_post')
        author_id = author.id

        # update name
        url = '/authors/{id:d}/'.format(id=author_id)
        response = self.app.put(url, data=data, follow_redirects=True)
        self.assertEqual(400, response.status_code)


class BookTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        AuthorModel.query.delete()
        BookModel.query.delete()
        BookAuthorM2M.query.delete()

    def tearDown(self):
        pass

    def add_author(self, test_name):
        author = AuthorModel(name=test_name, description=test_name)
        db_session.add(author)
        db_session.commit()

        return author

    def add_book(self, test_name, authors=[]):
        book = BookModel(name=test_name, description=test_name)
        db_session.add(book)
        db_session.commit()

        for author in authors:
            book.authors.append(author)

        return book

    def get_nonexisting_id(self, ModelClass):
        try:
            last_item = ModelClass.query.order_by('id')[-1]
            non_existing_id = last_item.id + 1
        except IndexError:
            non_existing_id = 1

        return non_existing_id

    def test_000_get_simple_200(self):
        authors = map(lambda x: self.add_author(x), ['000_A1', '000_A2', '000_A3'])
        book = self.add_book('book000', authors)

        book_id = book.id

        url = '/book/{id:d}/'.format(id=book_id)

        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.data)

        self.assertEqual('book000', response_data['name'])
        self.assertEqual('book000', response_data['description'])

        self.assertEqual(3, len(response_data['authors']))
        self.assertItemsEqual(['000_A1', '000_A2', '000_A3'], response_data['authors'])

    def test_001_get_nonexisting_book(self):
        non_existing_id = self.get_nonexisting_id(BookModel)

        url = '/book/{id:d}/'.format(id=non_existing_id)

        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(404, response.status_code)

    def test_002_get_book_without_authors(self):
        book = self.add_book('book002', [])
        book_id = book.id

        url = '/book/{id:d}/'.format(id=book_id)

        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data)
        self.assertEqual(0, len(response_data['authors']))

    def test_003_delete_book_200(self):
        authors = map(lambda x: self.add_author(x), ['003_A1', '003_A2', '003_A3'])
        book = self.add_book('book003', authors)
        book_id = book.id

        url = '/book/{id:d}/'.format(id=book_id)

        response = self.app.delete(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)

        book = BookModel.query.filter_by(id=book_id).first()
        self.assertIsNone(book)

    def test_004_delete_unexisting_book(self):
        non_existing_id = self.get_nonexisting_id(BookModel)

        url = '/book/{id:d}/'.format(id=non_existing_id)

        response = self.app.delete(url, follow_redirects=True)

        self.assertEqual(404, response.status_code)

    def test_005_post_create_simple_book_200(self):
        authors = map(lambda x: self.add_author(x), ['005_A1', '005_A2', '005_A3'])
        authors_id = map(lambda it: it.id, authors)
        data = {
            'name': 'test_005_post_create_simple_book',
            'description': 'test_005_post_create_simple_book',
            'authors': authors_id,
        }

        url = '/book/new/'

        response = self.app.post(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)

        new_book_id = int(response.data)

        book = BookModel.query.filter_by(id=new_book_id).first()

        self.assertIsNotNone(book)

        self.assertEqual('test_005_post_create_simple_book', book.name)
        self.assertEqual('test_005_post_create_simple_book', book.description)

        self.assertEqual(len(authors), len(book.authors))
        self.assertItemsEqual(authors, book.authors)

    def test_006_post_create_bad_data(self):
        authors = map(lambda x: self.add_author(x), ['006_A1', '006_A2', '006_A3'])
        authors_id = map(lambda it: it.id, authors)

        datas = [
            {},
            {'name': '123', 'authors': authors_id},
            {'description': '123', 'authors': authors_id},
            {'name': '123', 'description': '123'},
            {'name': None, 'description': '123', 'authors': authors_id},
            {'name': '123', 'description': None, 'authors': authors_id},
            {'name': '123', 'description': '123', 'authors': None},
            {'name': '123', 'description': '123', 'authors': authors_id, 'bad_param': '123'},
        ]
        url = '/book/new/'

        for data in datas:
            books_count_before = BookModel.query.count()
            response = self.app.post(url, data=json.dumps(data), follow_redirects=True)
            self.assertEqual(400, response.status_code)
            self.assertEqual(books_count_before, BookModel.query.count())

    def test_007_post_create_nonexisting_author(self):
        authors = map(lambda x: self.add_author(x), ['007_A1', '007_A2', '007_A3'])
        authors_id = map(lambda it: it.id, authors)
        nonexising_author_id = self.get_nonexisting_id(AuthorModel)
        authors_id.append(nonexising_author_id)

        data = {
            'name': 'test_007_post_create_nonexisting_author',
            'description': 'test_007_post_create_nonexisting_author',
            'authors': authors_id,
        }

        url = '/book/new/'

        response = self.app.post(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(404, response.status_code)

        # check for rollback
        self.assertEqual(3, AuthorModel.query.count())
        self.assertEqual(0, BookModel.query.count())
        self.assertEqual(0, BookAuthorM2M.query.count())

    def test_008_post_invalid_json_body(self):
        data = 'Its\' not a valid JSON \", really]'
        url = '/book/new/'

        response = self.app.post(url, data=data, follow_redirects=True)

        self.assertEqual(400, response.status_code)

    def test_009_put_simple_200(self):
        old_authors = map(lambda x: self.add_author(x), ['009_A1', '009_A2', '009_A3'])
        book = self.add_book('book009', old_authors)
        book_id = book.id

        new_authors = map(lambda x: self.add_author(x), ['009_NEW_A1', '009_NEW_A2'])
        new_authors_ids = map(lambda x: x.id, new_authors)

        url = '/book/{id:d}/'.format(id=book_id)
        data = {
            'name': 'new_book009_name',
            'description': 'new_book009_description',
            'authors': new_authors_ids
        }

        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)

        updated_book_object = BookModel.query.filter_by(id=book_id).first()
        self.assertIsNotNone(updated_book_object)
        self.assertEqual('new_book009_name', updated_book_object.name)
        self.assertEqual('new_book009_description', updated_book_object.description)
        self.assertEqual(len(new_authors), len(updated_book_object.authors))
        self.assertItemsEqual(new_authors, updated_book_object.authors)

    def test_010_put_single_field(self):
        old_authors = map(lambda x: self.add_author(x), ['010_A1', '010_A2', '010_A3'])

        # check name
        book1 = self.add_book('book010_1', old_authors)
        book_id = book1.id
        url = '/book/{id:d}/'.format(id=book_id)
        data = {
            'name': 'new_book010_name',
        }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)
        db_session.refresh(book1)
        self.assertEqual('new_book010_name', book1.name)
        self.assertEqual('book010_1', book1.description)
        self.assertItemsEqual(book1.authors, old_authors)

        # check description
        book2 = self.add_book('book010_2', old_authors)
        book_id = book2.id
        url = '/book/{id:d}/'.format(id=book_id)
        data = {
            'description': 'new_book010_description',
        }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)
        db_session.refresh(book2)
        self.assertEqual('book010_2', book2.name)
        self.assertEqual('new_book010_description', book2.description)
        self.assertItemsEqual(book2.authors, old_authors)

        # check authors
        book3 = self.add_book('book010_3', old_authors)
        new_authors = map(lambda x: self.add_author(x), ['010_A4', '010_A5', '010_A6', '010_A7'])
        book_id = book3.id
        url = '/book/{id:d}/'.format(id=book_id)
        data = {
            'authors': map(lambda x: x.id, new_authors),
        }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)
        db_session.refresh(book3)
        self.assertEqual('book010_3', book3.name)
        self.assertEqual('book010_3', book3.description)
        self.assertEqual(len(new_authors), len(book3.authors))
        self.assertItemsEqual(new_authors, book3.authors)

    def test_011_put_incorrect_request_400(self):
        old_authors = map(lambda x: self.add_author(x), ['011_A1', '011_A2', '011_A3'])

        book = self.add_book('book012', old_authors)

        datas = [
            {},
            {'authors': None},
            {'name': None},
            {'description': None},
            {'name': '123', 'description': '123', 'authors': [], 'bad_field': '123'},
        ]
        url = '/book/{id:d}/'.format(id=book.id)

        for data in datas:
            response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

            self.assertEqual(400, response.status_code)

    def test_012_put_not_existing_book(self):
        not_existing_id = self.get_nonexisting_id(BookModel)

        url = '/book/{id:d}/'.format(id=not_existing_id)
        data = {'name': '123'}

        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(404, response.status_code)

    def test_013_put_update_with_nonexisting_author(self):
        old_authors = map(lambda x: self.add_author(x), ['013_A1', '013_A2', '013_A3'])
        new_authors = map(lambda x: self.add_author(x), ['013_A4', '013_A5', '013_A6', '013_A7'])
        new_authors_ids = map(lambda it: it.id, new_authors)
        new_authors_ids.append(self.get_nonexisting_id(AuthorModel))

        book = self.add_book('book013', old_authors)
        url = '/book/{id:d}/'.format(id=book.id)
        data = {
            'authors': new_authors_ids,
        }

        old_m2m_count = BookAuthorM2M.query.count()

        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(404, response.status_code)
        self.assertEqual(len(old_authors) + len(new_authors), AuthorModel.query.count())
        self.assertEqual(1, BookModel.query.count())
        self.assertEqual(old_m2m_count, BookAuthorM2M.query.count())

    def test_014_put_invalid_json(self):
        old_authors = map(lambda x: self.add_author(x), ['014_A1', '014_A2', '014_A3'])
        book = self.add_book('book014', old_authors)

        url = '/book/{id:d}/'.format(id=book.id)
        data = 'Its\' not a valid JSON \", really]'

        response = self.app.put(url, data=data, follow_redirects=True)

        self.assertEqual(400, response.status_code)


class LibraryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        AuthorModel.query.delete()
        BookModel.query.delete()
        BookAuthorM2M.query.delete()

    def tearDown(self):
        pass

    def add_author(self, test_name):
        author = AuthorModel(name=test_name, description=test_name)
        db_session.add(author)
        db_session.commit()

        return author

    def add_book(self, test_name, authors=[]):
        book = BookModel(name=test_name, description=test_name)
        db_session.add(book)
        db_session.commit()

        for author in authors:
            book.authors.append(author)

        return book

    def get_nonexisting_id(self, ModelClass):
        try:
            last_item = ModelClass.query.order_by('id')[-1]
            non_existing_id = last_item.id + 1
        except IndexError:
            non_existing_id = 1

        return non_existing_id

    def test_000_get_simple(self):
        authors = map(lambda x: self.add_author(x), ['000_A1', '000_A2', '000_A3'])
        book = self.add_book('book000', authors)

        url = '/library/'
        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)

        response_data = json.loads(response.data)

        self.assertEqual(1, len(response_data))

    def test_001_get_more_that_one_page(self):
        authors = map(lambda x: self.add_author(x), ['000_A1', '000_A2', '000_A3'])

        for it in xrange(config.LIBRARY_PAGE_SIZE + 1):
            book_name = 'book%03d' % it
            book = self.add_book(book_name, authors)

        url = '/library/'
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data)
        self.assertEqual(config.LIBRARY_PAGE_SIZE, len(response_data))

        url = '/library/1/'
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data)
        self.assertEqual(config.LIBRARY_PAGE_SIZE, len(response_data))

        url = '/library/2/'
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data)
        self.assertEqual(1, len(response_data))

    def test_002_get_unexisting_page(self):
        authors = map(lambda x: self.add_author(x), ['000_A1', '000_A2', '000_A3'])
        book = self.add_book('book000', authors)

        url = '/library/2/'
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(404, response.status_code)


class LibraryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        AuthorModel.query.delete()
        BookModel.query.delete()
        BookAuthorM2M.query.delete()
        cache.clear()

    def tearDown(self):
        pass

    def add_author(self, test_name):
        author = AuthorModel(name=test_name, description=test_name)
        db_session.add(author)
        db_session.commit()

        return author

    def add_book(self, test_name, authors=[]):
        book = BookModel(name=test_name, description=test_name)
        db_session.add(book)
        db_session.commit()

        for author in authors:
            book.authors.append(author)

        return book

    def get_nonexisting_id(self, ModelClass):
        try:
            last_item = ModelClass.query.order_by('id')[-1]
            non_existing_id = last_item.id + 1
        except IndexError:
            non_existing_id = 1

        return non_existing_id

    def test_000_simple_call(self):
        authors = map(lambda x: self.add_author(x), ['000_A1', '000_A2', '000_A3'])
        book = self.add_book('book000', authors)

        url = '/statistics/'

        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)

    @timeout_decorator.timeout(10, timeout_exception=StopIteration)
    def test_000_1000_calls(self):
        authors = map(lambda x: self.add_author(x), ['000_A1', '000_A2', '000_A3'])
        book = self.add_book('book000', authors)

        url = '/statistics/'

        begin = datetime.datetime.now()

        for it in xrange(1000):
            response = self.app.get(url, follow_redirects=True)
            self.assertEqual(200, response.status_code)

        end = datetime.datetime.now()

        timedelta = end - begin

        self.assertEqual(0, timedelta.days)
        self.assertTrue(timedelta.seconds < 5)


if __name__ == '__main__':
    unittest.main()
