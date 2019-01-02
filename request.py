from urllib.parse import unquote_plus
from utils import (
    json_loads,
    formatted_dict,
)


def parsed_dict(data, sep, subsep):
    items = data.split(sep)
    d = {}
    for item in items:
        k, v = item.split(subsep, 1)
        d[k] = v

    return d


def parsed_query(path):
    if '?' in path:
        path, query = path.split('?', 1)
        query = {unquote_plus(k): unquote_plus(v) for k, v in parsed_dict(query, '&', '=').items()}
        return path, query
    else:
        return path, {}


def parsed_request_line(request_line):
    method, path, protocol = request_line.split(' ', 2)
    path, query = parsed_query(path)
    return method, path, query, protocol


def parsed_cookie(headers):
    if 'cookie' in headers:
        cookie = headers['cookie']
        cookie = parsed_dict(cookie, '; ', '=')
        return cookie
    else:
        return {}


def parsed_headers(header):
    headers = {k.lower(): v for k, v in parsed_dict(header, '\r\n', ': ').items()}
    cookie = parsed_cookie(headers)
    return headers, cookie


def parsed_head(head):
    head = head.decode('ascii')

    request_line, header = head.split('\r\n', 1)
    method, path, query, protocol = parsed_request_line(request_line)
    headers, cookie = parsed_headers(header)

    return method, path, query, protocol, headers, cookie


def parsed_body(body, headers):
    is_form_body = 'content-type' in headers and headers['content-type'] == 'application/x-www-form-urlencoded'
    is_json_body = 'content-type' in headers and headers['content-type'] == 'application/json'

    if is_form_body:
        body = body.decode('utf-8')
        data = {unquote_plus(k): unquote_plus(v) for k, v in parsed_dict(body, '&', '=').items()}
    elif is_json_body:
        body = body.decode('utf-8')
        data = json_loads(body)
    else:
        data = body

    return data


class Request(object):
    def __init__(self, data):
        head, body = data.split(b'\r\n\r\n', 1)

        method, path, query, protocol, headers, cookie = parsed_head(head)

        data = parsed_body(body, headers)

        self.method = method
        self.path = path
        self.query = query
        self.protocol = protocol
        self.headers = headers
        self.cookie = cookie
        self.data = data

    @classmethod
    def class_name(cls):
        return cls.__name__.lower()

    def __repr__(self):
        class_name = self.class_name()
        begin = f'<{class_name}>'
        end = f'</{class_name}>'

        d = self.__dict__
        data = formatted_dict(d)

        r = '\n'.join(['', begin, data, end, ''])
        return r
