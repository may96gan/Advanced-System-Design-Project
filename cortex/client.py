#!/usr/bin/python
import socket
import struct
import sys
import time

import requests

from google.protobuf.json_format import MessageToJson
from .cli import CommandLineInterface
from .Reader import Reader

cli = CommandLineInterface()


@cli.command
def upload(address, user, thought):
    upload_thought(address, user, thought)

def upload_sample(host, port, path):
    #conn = socket.socket()
    #address = host, port
    _configUrl = f'http://{host}:{port}/config'
    _snapUrl = f'http:/{host}:{port}/snapshot'
    _configRes = requests.get(_configUrl)
    parsers = _configRes.json().parsers
    print(f'in client got parsers = {parsers}')
    #conn.connect((address))
    reader = Reader(path)
    for snapshot in reader:
        _snapRes = requests.post(_snapUrl, MessageToJson(snapshot))



def upload_thought(address, user_id, thought):
    conn = socket.socket()
    if (isinstance(address, str)):
        adr = tuple(address.split(":"))
        h = adr[0]
        p = (int)(adr[1])
        address = h, p
    conn.connect((address))
    thought = bytes(thought, 'utf-8')
    packed_data = \
        struct.pack('LLI', (int)(user_id), (int)(time.time()), len(thought))
    conn.sendall(packed_data)
    conn.sendall(thought)
    print('done')
    conn.close()


def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        upload_thought(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
    print('done')
