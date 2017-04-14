#!/usr/bin/python

__author__ = "Joseph Mullen"

# Define the application directory
import os
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Look here for large application guidance https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
# is this what a config file should really look like? https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

"""Main config class- used for inheritance"""
class Config(object):
    DEBUG = True
    TESTING = False
    # Secret key for signing cookies
    SECRET_KEY = "secret"
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # database settings

# to be completed
#class ProductionConfig(Config):









