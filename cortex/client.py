#!/usr/bin/python
import socket
import struct
import sys
import time
import click 
import json
import requests

from google.protobuf.json_format import MessageToJson
from .cli import CommandLineInterface
from .Reader import Reader

cli = CommandLineInterface()
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



@cli.command
def upload(host, port, path):
    upload_sample(host, port, path)

@main.command('upload-sample')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('path', type=str)
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
    user = MessageToJson(reader.get_user())
    _userJ = json.loads(user)
    for snapshot in reader.read():
        #print("first snap")
        m = MessageToJson(snapshot)
        print(type(m))
        print(type(_userJ))
        _snapJ = json.loads(MessageToJson(snapshot))
        userAndSnap = user[:-1] +','+ m[1:]
        print(userAndSnap[0:100])
        _snapRes = requests.post(_snapUrl, userAndSnap)
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



if __name__ == '__main__':
    main()
    print('done')
