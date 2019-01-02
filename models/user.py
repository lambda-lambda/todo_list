from models import Model
from utils import log
import hashlib
import config


def hashed_password(password, salt=config.salt):
    salted_password = (password + salt).encode('utf-8')
    hash = hashlib.sha256(salted_password).hexdigest()
    return hash


def test_hashed_password():
    s = hashed_password('123')
    log('s', s, type(s))


class User(Model):
    def __init__(self, **options):
        super().__init__(**options)
        self.username = options['username']
        self.password = options['password']


def test_user_model():
    form = {
        'username': 'yuancjun',
        'password': '123',
    }

    form['password'] = hashed_password(form['password'])

    user = User.new(**form)
    log('user', user)
