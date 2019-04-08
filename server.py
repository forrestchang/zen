# -*- coding: utf-8 -*-
"""
    A simple server to run wsgi application.
"""

from werkzeug.serving import run_simple
from app import application

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5525

    run_simple(host, port, application, use_debugger=True, use_reloader=True)

