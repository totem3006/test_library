# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(config.PROJECT_NAME)
app.config.from_object('config')
db = SQLAlchemy(app)

from application import views, models
