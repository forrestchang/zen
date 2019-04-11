# -*- coding: utf-8 -*-

"""
    Zen, a simple web framework.
"""

STATUS_INFO = {
    200: 'OK',
    404: 'Not Found'
}


class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def path(self):
        return self.environ.get('PATH_INFO')

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
        return self._body.encode('utf-8')

    @body.setter
    def body(self, value):
        self._body = value


class Zen:
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()

        response.status_code = 200
        response.set_header('TEST', 'hello_world')
        response.body = 'Hello world'

        print(response.status)
        print(response.response_headers)
        print(response.body)
        start_response(response.status, response.response_headers)
        return [response.body]

