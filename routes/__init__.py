from response import Response


def static(request):
    query = request.query
    filename = query['filename']
    response = Response.new_static_response(filename)
    return response


def signin(request):
    response = Response.new_html_response('signin.html')
    return response


def signup(request):
    response =Response.new_html_response('signup.html')
    return response


def index(request):
    response = Response.new_html_response('index.html')
    return response


def init_routes():
    d = {
        '/static': static,
        '/signin': signin,
        '/signup': signup,
        '/': index,
    }

    return d
