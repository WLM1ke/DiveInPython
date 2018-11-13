import pathlib
import tempfile


class File:
    def __init__(self, path):
        self._path = path

    def __str__(self):
        return self.path

    def __add__(self, other):
        text = self.read() + other.read()
        path = str(pathlib.Path(tempfile.gettempdir()) / str(hash(self) ^ hash(other)))
        file = File(path)
        file.write(text)
        return file

    def __iter__(self):
        with open(self.path) as file:
            for line in file:
                yield line

    @property
    def path(self):
        return self._path

    def write(self, text):
        with open(self.path, 'w') as file:
            file.write(text)

    def read(self):
        with open(self.path) as file:
            return file.read()

    def delete(self):
        pathlib.Path(self.path).unlink()


if __name__ == '__main__':
    a = File('solution1.py')
    print(a)
    for line in a:
        print(line)
    b = File('solution1.py')
    c = a + b
    print(c)
    print(c.read())
    c.delete()
