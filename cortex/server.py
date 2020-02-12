#!/usr/bin/python
from pathlib import Path as path
import sys
import signal
import socket
import struct
from datetime import datetime
import threading
from cortex.cli import CommandLineInterface
from flask import Flask
from flask import request


cli = CommandLineInterface()


@cli.command
def run(address, data):
    run_serverOrig(address, data)



class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        packed_data = self.receive_data(self.connection, 20)
        user_id, timestamp, thought_size = struct.unpack('QQI', packed_data)
        thought = self.receive_data(self.connection, thought_size).\
            decode('utf-8')
        dt_object = datetime.fromtimestamp(timestamp)
        self.write_thought(user_id, dt_object, thought)

    def receive_data(self, connection, msgLen):
        received_buf = b''
        while 1:
            msg = self.connection.recv(msgLen)
            if not msg:
                raise Exception
            received_buf += msg
            if (len(received_buf) == msgLen):
                break
        return received_buf

    def write_thought(self, user_id, timestamp, thought):
        p = path(self.data_dir) / str(user_id)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
        fn = p / f'{timestamp:%Y-%m-%d_%H-%M-%S}.txt'
        self.lock.acquire()
        try:
            with open(fn, 'a') as out:
                if (out.tell() != 0):
                    thought = '\n' + thought
                out.write(thought)
        finally:
            self.lock.release()

class CortexHandler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, publishFunc):
        super().__init__()
        self.connection = connection
        self.publishFunc = publishFunc

    def run(self):
        packed_data = self.receive_data(self.connection, 20)
        user_id, timestamp, thought_size = struct.unpack('QQI', packed_data)
        thought = self.receive_data(self.connection, thought_size).\
            decode('utf-8')
        dt_object = datetime.fromtimestamp(timestamp)
        self.write_thought(user_id, dt_object, thought)

    def receive_data(self, connection, msgLen):
        received_buf = b''
        while 1:
            msg = self.connection.recv(msgLen)
            if not msg:
                raise Exception
            received_buf += msg
            if (len(received_buf) == msgLen):
                break
        return received_buf

    def write_thought(self, user_id, timestamp, thought):
        p = path(self.data_dir) / str(user_id)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
        fn = p / f'{timestamp:%Y-%m-%d_%H-%M-%S}.txt'
        self.lock.acquire()
        try:
            with open(fn, 'a') as out:
                if (out.tell() != 0):
                    thought = '\n' + thought
                out.write(thought)
        finally:
            self.lock.release()


def run_server(host, port, publish):
    publish = publish
    app = Flask(__name__)

    @app.route('/config', methods = ['GET'])
    def myParsers():
        #return this.parsers
        print("in server parsers")
        return "hello parsers"

    @app.route('/snapshot', methods = ['POST'])
    def newSnapshot():
        print("in server snapshot")
        snapshot = request.get_data()
        print(snapshot)
        #publish(snapshot)

    app.run(host = host,port = port,threaded=True)
    #server = socket.socket()
    #address = host, port
    #server.bind((address))
    #server.listen(1000)
    #try:
     #   while 1:
      #      client, client_address = server.accept()
       #     handler = CortexHandler(client, publish)
        #    handler.start()
    #finally:
    #    server.close()


def run_serverOrig(address, data_dir):
    server = socket.socket()
    if (isinstance(address, str)):
        adr = tuple(address.split(":"))
        h = adr[0]
        p = (int)(adr[1])
        address = h, p
    server.bind((address))
    server.listen(1000)
    try:
        while 1:
            client, client_address = server.accept()
            handler = Handler(client, data_dir)
            handler.start()
    finally:
        server.close()


def signal_handler(sig, frame):
    sys.exit(0)


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address>')
        return 1
    try:
        run_serverOrig(sys.argv[1], sys.argv[2])
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
