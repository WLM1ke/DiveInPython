import json
import functools


def to_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    return wrapper


@to_json
def get_data():
    return {'data': 42}


if __name__ == '__main__':
    assert get_data() == '{"data": 42}'
    print(get_data())
    assert get_data.__name__ == 'get_data'
    print(get_data.__name__)
