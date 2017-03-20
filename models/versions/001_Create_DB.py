# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import *
from migrate import *

meta = MetaData()

Author = Table(
    'Author', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('description', Text(), default=''),
)
Book = Table(
    'Book', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('description', Text(), default=''),
)
M2M = Table(
    'M2M', meta,
    Column('author_id', Integer, ForeignKey('Author.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('Book.id'), primary_key=True),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Author.create()
    Book.create()
    M2M.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    M2M.drop()
    Book.drop()
    Author.drop()
