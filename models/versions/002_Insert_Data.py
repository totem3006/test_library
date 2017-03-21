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

'''
    "Азбука" Иванов В.П.
    "Азбука (расширенное издание)" Иванов В.П., Сидоров С.С.
    "Война и Мир" Толстой Л.Н.
'''
def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Author.insert().values([
        {'id': 1, 'name': 'Иванов В.П.', 'description': 'Описание Иванова'},
        {'id': 2, 'name': 'Сидоров С.С.', 'description': 'Описание Петрова'},
        {'id': 3, 'name': 'Толстой Л.Н.', 'description': 'Описание Толстого'},
    ]).execute()

    Book.insert().values([
        {'id': 1, 'name': 'Азбука', 'description': 'Главная книга'},
        {'id': 2, 'name': 'Азбука (расширенное издание)', 'description': 'Расширенная главная книга'},
        {'id': 3, 'name': 'Война и Мир', 'description': 'Роман-Эпопея'},
    ]).execute()

    M2M.insert().values([
        {'author_id': 3, 'book_id': 3},
        {'author_id': 1, 'book_id': 1},
        {'author_id': 1, 'book_id': 2},
        {'author_id': 2, 'book_id': 2},
    ]).execute()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    M2M.delete().execute()
    Book.delete().execute()
    Author.delete().execute()
