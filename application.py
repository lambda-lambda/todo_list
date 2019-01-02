from server import process_request
from utils import log
import _thread
import socket


class Application(object):
    routes = {}

    @classmethod
    def run(cls, host="127.0.0.1", port=3001):
        with socket.socket() as s:
            s.bind((host, port))
            s.listen()
            log(f'server http://{host}:{port}/')

            while True:
                connection, address = s.accept()
                log('client {}:{}'.format(*address))

                routes = cls.routes
                _thread.start_new_thread(process_request, (connection, routes))
