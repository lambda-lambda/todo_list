from models import Model
from utils import log


class Todo(Model):
    def __init__(self, **options):
        super().__init__(**options)
        self.content = options['content']
        self.user_id = options['user_id']


def test_todo_model():
    form = {
        'content': '吃饭',
    }

    todo = Todo.new(**form)
    log('todo', todo)
