import sys


if __name__ == '__main__':
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])
    d = b ** 2 - 4 * a * c
    print(int((-b - d ** 0.5) / (2 * a)))
    print(int((-b + d ** 0.5) / (2 * a)))
