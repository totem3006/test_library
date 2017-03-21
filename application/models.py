# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from application import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.metadata.reflect(engine)
Base.query = db_session.query_property()


class AuthorModel(Base):
    __table__ = Table('Author', Base.metadata, autoload=True)

    def to_JSON(self):
        return json.dumps(
            {'name': self.name, 'description': self.description, },
            ensure_ascii=False
        ).encode('utf8')

    def __repr__(self):
        return '<Author %r (%d)>' % (self.name, self.id, )

class BookModel(Base):
    __table__ = Table('Book', Base.metadata, autoload=True)

class M2M(Base):
    __table__ = Table('M2M', Base.metadata, autoload=True)

