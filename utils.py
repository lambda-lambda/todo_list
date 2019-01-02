from datetime import (
    datetime,
    timedelta,
    timezone,
)

import os
import config
import json


def log(*args, **kwargs):
    path = log_file_path()
    with open(path, 'a', encoding='utf-8') as f:
        prompt = '>>>'
        dt = current_zh_datetime()
        print(dt, prompt, *args, **kwargs)
        print(dt, prompt, *args, **kwargs, file=f)


def project_root_path():
    path = os.path.realpath(__file__)
    root = os.path.dirname(path)
    return root


def log_file_path():
    root = project_root_path()
    path = os.path.join(root, config.log_file)
    return path


def template_file_path(filename):
    root = project_root_path()
    path = os.path.join(root, f'templates/{filename}')
    return path


def data_file_path(class_name):
    root = project_root_path()
    filename = f'{class_name}.json'
    path = os.path.join(root, f'data/{filename}')
    return path


def static_file_path(filename):
    root = project_root_path()
    path = os.path.join(root, f'static/{filename}')
    return path


def content_of_static_file(filename):
    path = static_file_path(filename)
    with open(path, mode='rb') as f:
        data = f.read()
        return data


def render_template(filename, **options):
    path = template_file_path(filename)
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        for k, v in options.items():
            s = s.replace(f'{{{{ {k} }}}}', v)

        return s


def current_zh_datetime():
    utc_now = datetime.utcnow()
    bj = timezone(timedelta(hours=8))
    now = utc_now.astimezone(bj)

    format = '%Y-%m-%d %H:%M:%S'
    s = now.strftime(format)
    return s


def current_timestamp():
    now = datetime.now()
    timestamp = int(now.timestamp())
    return timestamp


def json_loads(data):
    return json.loads(data)


def json_dumps(data):
    return json.dumps(data, ensure_ascii=False, indent=2)


def formatted_dict(d):
    items = []
    for k, v in d.items():
        if isinstance(k, str):
            k = f'"{k}"'

        if isinstance(v, str):
            v = f'"{v}"'

        item = f'    ({k}): ({v})'
        items.append(item)

    data = '\n'.join(items)
    return data


def test_current_zh_datetime():
    s = current_zh_datetime()
    log('s', s)


def test_current_timestamp():
    timestamp = current_timestamp()
    log('timestamp', timestamp)
