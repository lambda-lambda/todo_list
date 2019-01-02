from utils import log
from request import Request
from response import Response


def read_request_data(connection):
    chunks = []

    while True:
        buffer_size = 1024
        chunk = connection.recv(buffer_size)
        chunks.append(chunk)

        if len(chunk) < buffer_size:
            data = b''.join(chunks)
            return data


def default_404_response(request):
    path = request.path
    response = Response.new_html_response('404.html', path=path)
    response.set_status(404)
    return response


def response_for_path(request, routes):
    path = request.path
    route = routes.get(path, default_404_response)
    response = route(request)
    return response


def process_request(connection, routes):
    with connection:
        data = read_request_data(connection)
        request = Request(data)
        log('request', request)

        response = response_for_path(request, routes)
        log('response', response)
        connection.sendall(response.to_bytes())
