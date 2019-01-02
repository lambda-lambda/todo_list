from models import Model
from models.user import User

from utils import log


class Session(Model):
    def __init__(self, **options):
        super().__init__(**options)
        self.key = options['key']
        self.user_id = options['user_id']


def current_user(request):
    key = request.cookie.get('key', 'not found')
    log('current user key', key)
    if key == 'not found':
        return None
    else:
        session = Session.one(key=key)
        user = User.one(id=session.user_id)
        return user


def test_todo_model():
    form = {
        'key': '7ba4d23b-53cd-4b29-8cd0-54c85b0f73c8',
        'user_id': 1,
    }

    session = Session.new(**form)
    log('session', session)
