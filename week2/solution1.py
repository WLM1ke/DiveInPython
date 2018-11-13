import pathlib
import tempfile
import argparse
import json


if __name__ == '__main__':
    path = pathlib.Path(tempfile.gettempdir()) / 'storage.data'
    if path.exists():
        with open(path) as f:
            data = json.load(f)
    else:
        data = dict()

    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='Key to store or show')
    parser.add_argument('--val', help='Value to store')
    parser.add_argument('--clear', action='store_true', help='Clear')
    args = parser.parse_args()
    if args.clear:
        path.unlink()
    elif args.key and args.val:
        data.setdefault(args.key, []).append(args.val)
        with open(path, 'w') as f:
            json.dump(data, f)
    elif args.key:
        if data.get(args.key):
            print(', '.join(data[args.key]))
        else:
            print('')
