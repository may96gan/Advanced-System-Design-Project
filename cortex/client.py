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
def upload(host, port, path):
    upload_sample(host, port, path)

def upload_sample(host, port, path):
    #conn = socket.socket()
    #address = host, port
    print("MAY 1")
    _configUrl = f'http://{host}:{port}/config'
    print("MAY 2")
    _snapUrl = f'http://{host}:{port}/snapshot'
    print("MAY 3")
    #_configRes = requests.get(_configUrl)
    #print(_configRes.json())
    #parsers = _configRes.json().parsers
    #print("MAY 5")
    #print(f'in client got parsers = {parsers}')
    #conn.connect((address))
    reader = Reader(path)
    for snapshot in reader.read():
        #print("first snap")
        _snapRes = requests.post(_snapUrl, MessageToJson(snapshot))
        print(_snapRes)



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
        upload_sample(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    cli.main()
    print('done')
