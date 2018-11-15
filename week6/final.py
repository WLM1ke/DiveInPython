import asyncio

COMMAND_WRONG = 'error\nwrong command\n\n'
COMMAND_OK = 'ok\n{}\n'


class ClientServerProtocol(asyncio.Protocol):
    data = dict()

    def __init__(self):
        self.transport = None
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self, data):
        if data[-1] != '\n':
            return COMMAND_WRONG
        elif data[:4] == 'get ':
            return self.process_get(data[4:-1])
        elif data[:4] == 'put ':
            return self.process_put(data[4:-1])
        return COMMAND_WRONG

    def process_get(self, key):
        if key == '*':
            respond = self.get_all()
        else:
            respond = self.get_key(key)
        return self.ok_wrapper(respond)

    def get_key(self, key):
        respond = [f'{key} {value} {timestamp}\n' for timestamp, value in self.data.get(key, {}).items()]
        return ''.join(respond)

    def get_all(self):
        respond = [self.get_key(key) for key in self.data]
        return ''.join(respond)

    def process_put(self, data):
        blocks = data.split(' ')
        if len(blocks) != 3:
            return COMMAND_WRONG
        key, value, timestamp = blocks
        timestamp_value = self.data.setdefault(key, {})
        timestamp_value[timestamp] = value
        return self.ok_wrapper()

    @staticmethod
    def ok_wrapper(data=''):
        return COMMAND_OK.format(data)


def run_server(host, port):
    loop = asyncio.get_event_loop()
    server_cor = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(server_cor)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server('127.0.0.1', 8888)
