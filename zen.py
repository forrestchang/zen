# -*- coding: utf-8 -*-

"""
    Zen, a simple web framework.
"""

import re

STATUS_INFO = {
    200: 'OK',
    404: 'Not Found'
}


class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def path(self):
        return self.environ.get('PATH_INFO', '').rstrip('/')

    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD', 'GET').upper()

    @property
    def query_string(self):
        return self.environ.get('QUERY_STRING', '')

    @property
    def query(self):
        query = {}
        for elem in self.query_string.split('&'):
            key, value = elem.split('=')
            query[key] = value
        return query


class Response:
    def __init__(self):
        self.status_code = 200
        self.headers = {}
        self._body = None

    @property
    def status(self):
        return f'{self.status_code} {STATUS_INFO[self.status_code]}'

    @property
    def response_headers(self):
        return [(str(key), str(value)) for key, value in self.headers.items()]

    def set_header(self, key, value):
        self.headers[key] = value

    @property
    def body(self):
        if self._body:
            return str(self._body).encode('utf-8')

    @body.setter
    def body(self, value):
        self._body = value


class Context:
    def __init__(self, environ):
        self.request = Request(environ)
        self.response = Response()


class Zen:

    def __init__(self):
        self.route_processors = []

    def __call__(self, environ, start_response):
        ctx = Context(environ)

        for path, method, func in self.route_processors:
            if ctx.request.path == path:
                ctx.response.body = func()

        status = ctx.response.status
        headers = ctx.response.response_headers
        body = ctx.response.body
        start_response(status, headers)
        return [body]

    def route(self, path, method=None):
        if method is None:
            method = 'GET'

        def _decorator(func):
            self.route_processors.append((path, method, func))

        return _decorator

