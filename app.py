# -*- coding: utf-8 -*-

"""
    A wsgi application.
"""

from zen import Zen

app = Zen()


@app.route('/index', method='GET')
def index():
    return 'Hello world'

@app.route('/name', method='GET')
def name():
    return 'Zen'


@app.route('/add', method='GET')
def add():
    return 1 + 1

