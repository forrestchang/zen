"""app.py"""

import datetime
from zen import Zen

app = Zen()


@app.route('/', method='GET')
def index(request, response):
    return 'Hello world'


@app.route('/path', method='GET')
def path(request, response):
    return request.path


@app.route('/fib', method='GET')
def fib(request, response):
    num = request.query.get('num')
    print(request.query_string)

    if num is None:
        return 'Could not find num.'

    return fib_service(int(num))


@app.route('/time', method='GET')
def time(request, response):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response.set_header('TIME', now)
    return now

def fib_service(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fib_service(num - 1) + fib_service(num - 2)

