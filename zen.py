"""zen.py"""

from typing import Any, Callable, Dict, List, Tuple


class ZenException(Exception):
    """Zen Exception"""


class RouteError(ZenException):
    """Route Error"""


class HTTPError(ZenException):
    """HTTP Error"""


def abort(status_code: int) -> Exception:
    """Abort HTTP request"""
    return HTTPError(status_code)


class Request:
    """Basic Request object"""

    def __init__(self, environ: dict) -> None:
        self.environ = environ

    @property
    def path(self) -> str:
        """Get path info"""
        return self.environ.get("PATH_INFO", "")

    @property
    def method(self) -> str:
        """Get method info"""
        return self.environ.get("REQUEST_METHOD", "GET").upper()

    @property
    def query_string(self) -> str:
        """Get query string"""
        return self.environ.get("QUERY_STRING", "")

    @property
    def query(self) -> dict:
        """Get query dict"""
        query = {}
        for elem in self.query_string.split("&"):
            key, value = elem.split("=")
            query[key] = value
        return query


STATUS_INFO = {200: "OK", 404: "Not Found"}


class Response:
    """Basic Response object"""

    def __init__(self) -> None:
        self.status_code = 200
        self._headers: Dict = {}
        self._body = None

    @property
    def status(self) -> str:
        """Get status"""
        return f"{self.status_code} {STATUS_INFO[self.status_code]}"

    @property
    def headers(self) -> List[Tuple[str, str]]:
        """Get headers"""
        return [(str(key), str(value)) for key, value in self._headers.items()]

    @property
    def body(self) -> bytes:
        """Get body"""
        if isinstance(self._body, bytes):
            return self._body
        return str(self._body).encode("utf-8")

    @body.setter
    def body(self, value: Any) -> None:
        """Set body"""
        self._body = value

    def set_header(self, key: str, value: str) -> None:
        """Set headers"""
        self._headers[key] = value


class Zen:
    """Zen web framework"""

    def __init__(self) -> None:
        self.route_processor: List = []

    def __call__(self, environ: dict, start_response: Callable) -> List[bytes]:
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
            response.body = "Not Found"  # type: ignore

        status = response.status
        headers = response.headers
        body = response.body

        start_response(status, headers)
        return [body]

    def route(self, path, method: str = None) -> Callable:
        """Route decoractor"""
        if method is None:
            method = "GET"

        def _decoractor(func):
            self.route_processor.append((path, method, func))

        return _decoractor

    def get(self, path: str) -> Callable:
        """Get method"""
        return self.route(path, "GET")

    def post(self, path: str) -> Callable:
        """Post method"""
        return self.route(path, "POST")

    def put(self, path: str) -> Callable:
        """Put method"""
        return self.route(path, "PUT")
