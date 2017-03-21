# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest
import tempfile
import json

import config

from application import app
from application.models import db_session
from application.models import AuthorModel



class AuthorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

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
        author = AuthorModel.query.order_by('id')[-1]
        non_existing_id = author.id + 1
        url = '/authors/{id:d}/'.format(id=non_existing_id)
        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(404, response.status_code)

    def test_003_update_user_200(self):
        author = self.add_author('test_003_update_user_200')

        url = '/authors/{id:d}/'.format(id=author.id)
        data = {'name': 'newname003', 'description': 'newdescription003'}
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)

    def test_004_update_user_both_fields(self):
        author = self.add_author('test_004_update_user_both_fields')
        author_id=author.id

        url = '/authors/{id:d}/'.format(id=author.id)
        data = {'name': 'newname004', 'description': 'newdescription004'}
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()

        author_name = author.name
        author_description = author.description

        self.assertEqual('newname004', author_name)
        self.assertEqual('newdescription004', author_description)

    def test_005_update_single_field(self):
        author = self.add_author('test_005_update_single_field')
        author_id=author.id

        # update name
        url = '/authors/{id:d}/'.format(id=author.id)
        data = {'name': 'newname005', }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()

        author_name = author.name
        author_description = author.description
        self.assertEqual('newname005', author_name)
        self.assertEqual('test_005_update_single_field', author_description)

        author.name = 'test_005_update_single_field'
        db_session.add(author)
        db_session.commit()

        # update description
        data = {'description': 'newdescription005', }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()
        author_name = author.name
        author_description = author.description
        self.assertEqual('test_005_update_single_field', author_name)
        self.assertEqual('newdescription005', author_description)

    ########################################################
    def test_006_update_bad_requests_400(self):
        author = self.add_author('test_006_update_bad_requests_400')
        author_id=author.id

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
            self.assertEqual('test_006_update_bad_requests_400', author.name)
            self.assertEqual('test_006_update_bad_requests_400', author.description)


    def test_009_update_nonexisting_author(self):
        author = AuthorModel.query.order_by('id')[-1]
        non_existing_id = author.id + 1
        url = '/authors/{id:d}/'.format(id=non_existing_id)

        data = {'name': 'NewName009', }
        response = self.app.put(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(404, response.status_code)

    def test_010_delete_200(self):
        author = self.add_author('test_010_delete_200')

        url = '/authors/{id:d}/'.format(id=author.id)
        response = self.app.delete(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)

    def test_011_successfully_delete(self):
        author = self.add_author('test_011_successfully_delete')
        author_id = author.id

        url = '/authors/{id:d}/'.format(id=author.id)
        response = self.app.delete(url, follow_redirects=True)

        author = AuthorModel.query.filter_by(id=author_id).first()

        self.assertIsNone(author)

    def test_012_delete_unexising_user(self):
        author = AuthorModel.query.order_by('id')[-1]
        non_existing_id = author.id + 1
        url = '/authors/{id:d}/'.format(id=non_existing_id)

        data = {'name': 'NewName009', }
        response = self.app.delete(url, follow_redirects=True)

        self.assertEqual(404, response.status_code)


    def test_013_post_good_params_and_200(self):
        url = '/authors/new/'

        data = {'name': 'test_013_post_good_params_and_200', 'description': 'test_013_post_good_params_and_200'}
        response = self.app.post(url, data=json.dumps(data), follow_redirects=True)

        self.assertEqual(200, response.status_code)

        new_object_id = int(response.data)

        author = AuthorModel.query.filter_by(id=new_object_id).first()
        self.assertIsNotNone(author)

        self.assertEqual('test_013_post_good_params_and_200', author.name)
        self.assertEqual('test_013_post_good_params_and_200', author.description)

    def test_014_bad_requests_examples(self):
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

    def test_015_non_json_for_put_and_post(self):
        url = '/authors/new/'

        data = 'It\'s not a json'
        response = self.app.post(url, data=data, follow_redirects=True)
        self.assertEqual(400, response.status_code)

        author = self.add_author('test_015_non_json_for_put_and_post')
        author_id=author.id

        # update name
        url = '/authors/{id:d}/'.format(id=author_id)
        response = self.app.put(url, data=data, follow_redirects=True)
        self.assertEqual(400, response.status_code)

if __name__ == '__main__':
    unittest.main()
