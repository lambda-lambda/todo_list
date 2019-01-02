from utils import (
    formatted_dict,
    render_template,
    content_of_static_file,
)

import json


def content_type_by_filename(filename):
    suffix = filename.split('.', 1)[1]

    d = {
        'js': 'application/javascript',
        'css': 'text/css',
        'jpg': 'image/jpeg',
        'png': 'image/png',
    }

    return d[suffix]


class Response(object):
    reasons = {
        200: "OK",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }

    def __init__(self):
        self.protocol = 'HTTP/1.1'
        self.status = 200
        self.status_text = 'OK'
        self.headers = {}
        self.cookie = {}
        self.body = ''
        self.data = b''

    def set_status(self, status):
        self.status = status
        self.status_text = self.reasons[status]

    @classmethod
    def new_html_response(cls, filename, **options):
        response = cls()
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.body = render_template(filename, **options)
        return response

    @classmethod
    def new_static_response(cls, filename):
        response = cls()
        response.headers['Content-Type'] = content_type_by_filename(filename)
        response.data = content_of_static_file(filename)
        return response

    @classmethod
    def new_json_response(cls, data):
        response = cls()
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        body = json.dumps(data)
        response.body = body
        return response

    @classmethod
    def new_403_response(cls):
        response = cls()
        response.set_status(403)
        response.body = render_template('403.html')
        return response

    def to_bytes(self):
        response_line = ' '.join([self.protocol, str(self.status), self.status_text])
        headers = '\r\n'.join([f'{k}: {v}' for k, v in self.headers.items()])

        def template_cookie(k, v):
            max_age = 60 * 5
            return f'Set-Cookie: {k}={v}; HttpOnly; SameSite=Strict; Max-Age={max_age}; Path=/'
            # return f'Set-Cookie: {k}={v}; HttpOnly; Max-Age={max_age}; Path=/'

        cookie = '\r\n'.join([template_cookie(k, v) for k, v in self.cookie.items()])

        if len(cookie) > 0:
            head = '\r\n'.join([response_line, headers, cookie])
        else:
            head = '\r\n'.join([response_line, headers])

        body = self.body
        if len(body) > 0:
            data = body.encode('utf-8')
        else:
            data = self.data

        head = head.encode('ascii')
        r = b'\r\n'.join([head, b'', data])
        return r

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
