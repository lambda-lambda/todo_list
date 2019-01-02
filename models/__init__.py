from utils import (
    data_file_path,
    current_timestamp,
    formatted_dict,
)

import json


def load_models(class_name):
    path = data_file_path(class_name)
    with open(path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def dump_models(class_name, data):
    path = data_file_path(class_name)
    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class Model(object):
    def __init__(self, **options):
        self.id = options['id']
        self.deleted = options['deleted']
        self.created_time = options['created_time']
        self.updated_time = options['updated_time']

    @classmethod
    def class_name(cls):
        return cls.__name__.lower()

    def test(self, **options):
        options['deleted'] = False
        d = self.__dict__
        for k, v in options.items():
            if d[k] != v:
                return False

        return True

    @classmethod
    def load_models(cls):
        class_name = cls.class_name()
        data = load_models(class_name)
        ms = [cls(**d) for d in data]
        return ms

    @classmethod
    def all(cls, **options):
        ms = cls.load_models()
        rs = []
        for m in ms:
            if m.test(**options):
                rs.append(m)
        return rs

    @classmethod
    def one(cls, **options):
        ms = cls.load_models()
        for m in ms:
            if m.test(**options):
                return m

    @classmethod
    def next_id(cls):
        ms = cls.load_models()
        if len(ms) == 0:
            return 1
        else:
            id = ms[-1].id + 1
            return id

    def save(self):
        ms = self.load_models()
        ms.append(self)
        self.dump_models(ms)

    @classmethod
    def new(cls, **options):
        options['id'] = cls.next_id()
        options['deleted'] = False
        timestamp = current_timestamp()
        options['created_time'] = timestamp
        options['updated_time'] = timestamp

        m = cls(**options)
        m.save()
        return m

    @classmethod
    def dump_models(cls, ms):
        class_name = cls.class_name()
        data = [m.__dict__ for m in ms]
        dump_models(class_name, data)

    @classmethod
    def delete(cls, id):
        m = cls.update(id, deleted=True)
        return m

    def update_fields(self, **options):
        for k, v in options.items():
            setattr(self, k, v)

        timestamp = current_timestamp()
        setattr(self, 'updated_time', timestamp)

    @classmethod
    def update(cls, id, **options):
        ms = cls.load_models()
        for m in ms:
            if m.test(id=id):
                m.update_fields(**options)
                cls.dump_models(ms)
                return m

    def __repr__(self):
        class_name = self.class_name()
        begin = f'<{class_name}>'
        end = f'</{class_name}>'

        d = self.__dict__
        data = formatted_dict(d)

        r = '\n'.join(['', begin, data, end, ''])
        return r

    def to_dict(self):
        d = self.__dict__
        d.pop('deleted')
        return d
