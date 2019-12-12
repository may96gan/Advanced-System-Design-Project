import socket


class Connection:
    def __init__(self, socket):
        self.conn = socket
        self.ip, self.port = socket.getpeername()
        self.other_ip, self.other_port = socket.getsockname()

    def __repr__(self):
        return f'<Connection from {self.other_ip}:{self.other_port} \
                    to {self.ip}:{self.port}>'

    def close(self):
        self.conn.close()

    def send(self, data):
        self.conn.sendall(data)

    def receive(self, size):
        data = b''
        while True:
            buf = self.conn.recv(size)
            if not buf:
                raise Exception
            data += buf
            if len(data) == size:
                break
        return data

    def connect(host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)

    def __enter__(self):
        pass

    def __exit__(self, exception, error, traceback):
        self.close()
