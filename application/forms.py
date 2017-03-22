# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import wtforms_json

from wtforms.form import Form
from wtforms.validators import Length
from wtforms.validators import Required
from wtforms.validators import NoneOf
from wtforms import TextField
from wtforms import FieldList
from wtforms import IntegerField


wtforms_json.init()


class AuthorCreateForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextField('description', validators=[Required(), Length(0, 255)])


class AuthorUpdateForm(Form):
    name = TextField('name')
    description = TextField('description', validators=[Length(0, 255)])

    def validate(self, *args, **kwargs):
        result = super(AuthorUpdateForm, self).validate(*args, **kwargs)

        if result:
            if (self.data['name'] is None) and (self.data['description'] is None):
                result = False

        return result


class BookCreateForm(Form):
    name = TextField('name', validators=[Required()])
    description = TextField('description', validators=[Required(), Length(0, 255)])
    authors = FieldList(
        IntegerField('authors', validators=[lambda y, x: x > 0]), validators=[Required()])


class BookUpdateForm(Form):
    name = TextField('name')
    description = TextField('description', validators=[Length(0, 255)])
    authors = FieldList(IntegerField('authors', validators=[lambda y, x: x > 0]))

    def validate(self, *args, **kwargs):
        result = super(BookUpdateForm, self).validate(*args, **kwargs)

        if result:
            if not(bool(self.name.data) or bool(self.description.data) or bool(self.authors.data)):
                # here is a bug (or feature?)
                # is {'authors': []} a valid JSON?
                result = False

        return result
