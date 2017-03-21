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

    def test_000_get_response_200(self):
        author = AuthorModel(name='Test000', description='Test000')
        db_session.add(author)
        db_session.commit()

        url = '/authors/{id:d}'.format(id=author.id)
        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)


    def test_001_get_normal_json_validate(self):
        author = AuthorModel(name='Test001', description='Test001')
        db_session.add(author)
        db_session.commit()

        url = '/authors/{id:d}'.format(id=author.id)
        response = self.app.get(url, follow_redirects=True)

        json_author = json.loads(response.data, encoding='utf8')

        author_name = json_author['name']
        author_description = json_author['description']

        self.assertEqual(author_name, 'Test001')
        self.assertEqual(author_description, 'Test001')

    def test_002_non_existing_author(self):

        author = AuthorModel.query.order_by('id')[-1]
        non_existing_id = author.id + 1
        url = '/authors/{id:d}'.format(id=non_existing_id)
        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(404, response.status_code)

if __name__ == '__main__':
    unittest.main()
