#!/usr/bin/python

__author__ = "Joseph Mullen"

from wtforms import Form, StringField, validators,  TextAreaField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

class queryForm(Form):
    WTF_CSRF_SECRET_KEY = 'a random string'
    queryString = TextAreaField('', widget=TextArea(), validators=[InputRequired()])



