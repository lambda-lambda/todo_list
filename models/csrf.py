from models import Model
from utils import log


class CSRF(Model):
    def __init__(self, **options):
        super().__init__(**options)
        self.key = options['key']


def test_csrf_model():
    form = {
        'key': '2b003c87-7545-402e-ada5-22a5c314f3ef',
    }

    csrf = CSRF.new(**form)
    log('csrf', csrf)
