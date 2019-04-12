"""zen.py"""


class ZenException(Exception):
    pass


class RouteError(ZenException):
    pass


class HTTPError(ZenException):
    pass


def abort(status_code):
    raise HTTPError(status_code)


class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def path(self):
        return self.environ.get('PATH_INFO', '')

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


STATUS_INFO = {
    200: 'OK',
    404: 'Not Found'
}


class Response:
    def __init__(self):
        self.status_code = 200
        self._headers = {}
        self._body = None

    @property
    def status(self):
        return f'{self.status_code} {STATUS_INFO[self.status_code]}'

    @property
    def headers(self):
        return [(str(key), str(value)) for key, value in self._headers.items()]

    @property
    def body(self):
        if isinstance(self._body, bytes):
            return self._body
        return str(self._body).encode('utf-8')

    @body.setter
    def body(self, value):
        self._body = value

    def set_header(self, key, value):
        self._headers[key] = value


class Zen:
    def __init__(self):
        self.route_processor = []

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response()

        matched = False

        for path, method, func in self.route_processor:
            if request.path == path and request.method == method:
                matched = True
                response.status_code = 200
                result = func(request, response)
                if not result:
                    raise HTTPError
                response.body = result

        if not matched:
            response.status_code = 404
            response.body = 'Not Found'

        status = response.status
        headers = response.headers
        body = response.body

        start_response(status, headers)
        return [body]

    def route(self, path, method=None):
        if method is None:
            method = 'GET'

        def _decoractor(func):
            self.route_processor.append((path, method, func))

        return _decoractor

    def get(self, path):
        return self.route(path, 'GET')

    def post(self, path):
        return self.route(path, 'POST')

    def put(self, path):
        return self.route(path, 'PUT')
