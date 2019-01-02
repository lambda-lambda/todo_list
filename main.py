from application import Application
from api.todo import init_routes as todo_api
from routes.todo import init_routes as todo_routes
from routes import init_routes as public_routes

from api.user import init_routes as user_api

from pprint import pprint


def init_application():
    application = Application()
    application.routes.update(todo_api())
    application.routes.update(todo_routes())
    application.routes.update(public_routes())
    application.routes.update(user_api())

    routes = {k: v.__name__ for k, v in application.routes.items()}
    pprint(routes)
    return application


if __name__ == '__main__':
    app = init_application()
    app.run()
