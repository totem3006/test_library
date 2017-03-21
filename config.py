# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

PROJECT_NAME = 'TLB'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILENAME = os.path.join(PROJECT_DIR, 'project.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{filename:s}'.format(filename=DB_FILENAME)
SQLALCHEMY_MIGRATE_REPO = os.path.join(PROJECT_DIR, 'models')
SQLALCHEMY_TRACK_MODIFICATIONS = True
