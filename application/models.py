# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from application import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.metadata.reflect(engine)
Base.query = db_session.query_property()

AuthorTable = Table('Author', Base.metadata, autoload=True)
BookTable = Table('Book', Base.metadata, autoload=True)
M2MTable = Table('M2M', Base.metadata, autoload=True)


class AuthorModel(Base):
    __table__ = AuthorTable

    def to_dict(self):
        return {'name': self.name, 'description': self.description, }

    def to_JSON(self):
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False
        ).encode('utf8')

    def __repr__(self):
        return '<Author %r (%d)>' % (self.name, self.id, )


class BookAuthorM2M(Base):
    __table__ = M2MTable


class BookModel(Base):
    __table__ = BookTable
    authors = relationship('AuthorModel', secondary=M2MTable, backref='Book')

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'authors': map(lambda it: it.name, self.authors)
        }

    def to_JSON(self):
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False
        ).encode('utf8')


