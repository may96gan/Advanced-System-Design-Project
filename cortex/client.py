#!/usr/bin/python
import socket
import struct
import sys
import time
import click 
import json
import requests

from google.protobuf.json_format import MessageToJson
from .Reader import Reader


@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass


def upload_sample(host, port, path):
    _configUrl = f'http://{host}:{port}/config'
    _snapUrl = f'http://{host}:{port}/snapshot'
    reader = Reader(path)
    user = MessageToJson(reader.get_user())
    #_userJ = json.loads(user)
    for snapshot in reader.read():
        m = MessageToJson(snapshot)
        #_snapJ = json.loads(MessageToJson(snapshot))
        userAndSnap = user[:-1] +','+ m[1:]
        _snapRes = requests.post(_snapUrl, userAndSnap)

@main.command('upload-sample')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('path', type=str)
def upload_sample_cli(host,port,path):
    upload_sample(host,port,path)

if __name__ == '__main__':
    main()
    print('done')
