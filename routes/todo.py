from response import Response
from auth import login_required


def index(request):
    response = Response.new_html_response('todo_index.html')
    return response


def init_routes():
    d = {
        '/todo/index': login_required(index),
    }

    return d
