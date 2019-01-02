from models.todo import Todo
from models.session import current_user

from response import Response
from auth import (
    login_required,
    same_user_required,
)


def add(request):
    user = current_user(request)
    form = request.data
    form['user_id'] = user.id
    todo = Todo.new(**form)
    response = Response.new_json_response(todo.to_dict())
    return response


def delete(request):
    query = request.query
    id = int(query['id'])
    todo = Todo.delete(id)
    response = Response.new_json_response(todo.to_dict())
    return response


def update(request):
    form = request.data
    id = form['id']
    content = form['content']
    todo = Todo.update(id, content=content)
    response = Response.new_json_response(todo.to_dict())
    return response


def all(request):
    query = request.query
    user = current_user(request)
    query['user_id'] = user.id
    todos = Todo.all(**query)
    todos = [todo.to_dict() for todo in todos]
    response = Response.new_json_response(todos)
    return response


def init_routes():
    d = {
        '/api/todo/add': login_required(add),
        '/api/todo/delete': login_required(same_user_required(delete, Todo)),
        '/api/todo/update': login_required(same_user_required(update, Todo)),
        '/api/todo/all': login_required(all),
    }

    return d
