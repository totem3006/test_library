# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import unittest
import tempfile

import config

from application import app
from application import db
from application.models import AuthorModel


class AuthorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_response_200(self):
        author = AuthorModel(name='Test', description='Test')
        db.session.add(author)
        db.session.commit()

        url = '/authors/{id:d}'.format(id=author.id)
        response = self.app.get(url, follow_redirects=True)

        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
