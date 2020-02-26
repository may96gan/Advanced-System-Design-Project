#!/usr/bin/python
from pathlib import Path as path
import sys
import signal
import socket
import struct
from datetime import datetime
import threading
from flask import Flask
from flask import request
import pika
import click 
import json

class Log:
    
    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info(): # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()

@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback





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

@main.command('run-server')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('publish', default='rabbitmq://127.0.0.1:5672/')
def run_server(host, port, publish):
    publish = publish
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='current_snapshots')
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
        channel.basic_publish(exchange='',
                              routing_key='current_snapshots',
                              body=snapshot)
        mj = json.loads(snapshot)
        if mj:
            print(mj['feelings'])
            print(mj['username'])
        print("done")
        return "ok"
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


if __name__ == '__main__':
    main()
