# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import config

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

Base = declarative_base()
Base.metadata.reflect(engine)


class AuthorModel(Base):
    __table__ = Table('Author', Base.metadata, autoload=True)

class BookModel(Base):
    __table__ = Table('Book', Base.metadata, autoload=True)

class M2M(Base):
    __table__ = Table('M2M', Base.metadata, autoload=True)

