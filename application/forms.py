# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import wtforms_json

from wtforms.form import Form
from wtforms.validators import Length
from wtforms.validators import Required
from wtforms.validators import NoneOf
from wtforms import TextField
from wtforms import SelectMultipleField


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
    authors = SelectMultipleField('authors', validators=[Required()])

    def validate_authors(self, field):
        print field
        assert False
        return True
