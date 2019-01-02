from models.user import (
    User,
    hashed_password,
)

from models.session import Session

from response import Response

import uuid


def signup(request):
    form = request.data
    form['password'] = hashed_password(form['password'])
    user = User.new(**form)
    response = Response.new_json_response(user.to_dict())
    return response


def delete(request):
    query = request.query
    id = int(query['id'])
    user = User.delete(id)
    response = Response.new_json_response(user.to_dict())
    return response


def update_username(request):
    form = request.data
    id = form['id']
    username = form['username']
    user = User.one(username=username)
    if user is None:
        u = User.update(id, username=username)
        response = Response.new_json_response(u.to_dict())
        return response
    else:
        response = Response.new_403_response()
        return response


def update_password(request):
    form = request.data
    id = form['id']
    old_password = hashed_password(form['old_password'])
    new_password = hashed_password(form['new_password'])
    user = User.one(id=id)
    if user.password == old_password:
        u = User.update(id, password=new_password)
        response = Response.new_json_response(u.to_dict())
        return response
    else:
        response = Response.new_403_response()
        return response


def all(request):
    query = request.query
    users = User.all(**query)
    users = [user.to_dict() for user in users]
    response = Response.new_json_response(users)
    return response


def signin(request):
    form = request.data
    form['password'] = hashed_password(form['password'])
    user = User.one(**form)
    key = str(uuid.uuid4())
    Session.new(key=key, user_id=user.id)
    response = Response.new_json_response(user.to_dict())
    response.cookie = {
        'key': key,
    }
    return response


def init_routes():
    d = {
        '/api/user/signin': signin,
        '/api/user/signup': signup,
        '/api/user/delete': delete,
        '/api/user/username/update': update_username,
        '/api/user/password/update': update_password,
        '/api/user/all': all,
    }

    return d
