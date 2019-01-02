import functools

from models.session import current_user
from response import Response


def login_required(route):
    @functools.wraps(route)
    def wrapped_route(request):
        user = current_user(request)
        if user is None:
            return Response.new_403_response()
        else:
            return route(request)

    return wrapped_route


def id_from_request(request):
    query = request.query
    data = request.data
    if 'id' in query:
        id = int(query['id'])
        return id
    elif 'id' in data:
        id = int(data['id'])
        return id
    else:
        return -1


def same_user_required(route, cls):
    @functools.wraps(route)
    def wrapped_route(request):
        user = current_user(request)
        if user is None:
            return Response.new_403_response()
        else:
            id = id_from_request(request)
            m = cls.one(id=id)
            if m.user_id == user.id:
                return route(request)
            else:
                return Response.new_403_response()

    return wrapped_route
