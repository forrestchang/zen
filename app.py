# -*- coding: utf-8 -*-

"""
    Zen, a simple web framework.
"""

def application(environ, start_response):
    response_body = b'Hello, World'
    status = '200 OK'
    start_response(status, response_headers=[])
    return [response_body]

