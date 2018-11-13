import sys

if __name__ == '__main__':
    sum_ = 0
    for n in sys.argv[1]:
        sum_ += int(n)
    print(sum_)
