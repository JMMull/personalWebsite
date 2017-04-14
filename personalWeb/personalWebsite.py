#!/usr/bin/python

__author__ = "Joseph Mullen"

# look here for setup deets http://stackoverflow.com/questions/12044776/how-to-use-flask-sqlalchemy-in-a-celery-task

from flask import Flask


app = Flask(__name__, static_url_path='/static')
app.config.from_object('config.Config')

import personal_web.views.pages