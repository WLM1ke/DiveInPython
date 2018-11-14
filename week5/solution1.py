import operator
import re
import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, ip, port, timeout=None):
        self.connection = socket.create_connection((ip, port), timeout)

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or str(int(time.time()))
        request = f'put {key} {value} {timestamp}\n'
        self.send_request(request)

    def get(self, key):
        request = f'get {key}\n'
        data = self.send_request(request)
        return self.parse_data(data)

    def send_request(self, request):
        connection = self.connection
        connection.sendall(request.encode())
        respond = connection.recv(4096).decode()
        if respond == 'error\nwrong command\n\n':
            raise ClientError
        return respond[3:-1]

    @staticmethod
    def parse_data(data):
        if not data:
            return dict()
        pattern = r'(\S+)\s(\S+)\s(\S+)\n'
        result = re.findall(pattern, data)
        result_formatted = ((key, float(value), int(timestamp)) for key, value, timestamp in result)
        result_sorted = sorted(result_formatted, key=operator.itemgetter(2))
        result_dict = dict()
        for key, value, timestamp in result_sorted:
            result_dict.setdefault(key, []).append((timestamp, value))
        return result_dict

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    data_ = 'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'
    print(Client.parse_data(data_[3:-1]))
