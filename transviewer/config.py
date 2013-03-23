#!/usr/bin/env python

# http://flask.pocoo.org/docs/config/#development-production

import os

class Config(object):
    SITE_NAME = 'tbbttrans'
    SECRET_KEY = "your app secret key"
    SYS_ADMINS = ['yourname@domain.com']

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///test.db')
    SQLALCHEMY_ECHO = False
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_ECHO = False

