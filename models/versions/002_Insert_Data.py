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

AUTHORS_FIXTURES = [
    {'name': 'Иванов В.П.', 'description': 'Описание Иванова'},
    {'name': 'Сидоров С.С.', 'description': 'Описание Петрова'},
    {'name': 'Толстой Л.Н.', 'description': 'Описание Толстого'},
]
BOOKS_FIXTURES = [
    {'name': 'Азбука', 'description': 'Главная книга'},
    {'name': 'Азбука (расширенное издание)', 'description': 'Расширенная главная книга'},
    {'name': 'Война и Мир', 'description': 'Роман-Эпопея'},
]
M2M_FIXTURE = [
    {'book': 'Азбука', 'name': 'Иванов В.П.'},
    {'book': 'Азбука (расширенное издание)', 'name': 'Иванов В.П.'},
    {'book': 'Азбука (расширенное издание)', 'name': 'Сидоров С.С.'},
    {'book': 'Война и Мир', 'name': 'Толстой Л.Н.'},
]


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    Author.insert().values(AUTHORS_FIXTURES).execute()
    Book.insert().values(BOOKS_FIXTURES).execute()

    for it in M2M_FIXTURE:
        name = it['name']
        book = it['book']

        author_id = Author.select(Author.c.name == name).execute().first()[0]
        book_id = Book.select(Book.c.name == book).execute().first()[0]

        M2M.insert().values({'author_id': author_id, 'book_id': book_id, }).execute()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    M2M.delete().execute()
    Book.delete().execute()
    Author.delete().execute()
