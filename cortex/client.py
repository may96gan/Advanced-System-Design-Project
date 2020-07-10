#!/usr/bin/python
import socket
import struct
import sys
import time
import click 
import json
import requests
import PIL
from pathlib import Path
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
    u_id = reader.get_user().user_id
    #print(u_id)
    user = MessageToJson(reader.get_user())
    #print(user)
    #_userJ = json.loads(user)
    for snapshot in reader.read():
        #print("may")
        #print(snapshot)
        #print(snapshot.pose)
        #print(snapshot.color_image)
        #print(snapshot.color_image.width)
        #print("*********************************************************")
        #print(snapshot.color_image.height)
        #print("*********************************************************")
        #print(snapshot.color_image.data)
        #print("*********************************************************")
        size = snapshot.color_image.width, snapshot.color_image.height
        #img = PIL.Image.frombytes('RGB', size,snapshot.color_image.data)
        #img.save('/home/user/Downloads/mi.png')
        #img.save('/home/user/Downloads/m1i.jpg')
        #print("sabe")
        datet = snapshot.datetime
        p = Path("snapshots_data") / str(u_id) / str(datet)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
        fn = p / 'color.txt'
        with open(fn, 'wb') as con:
            con.write(snapshot.color_image.data)
        #p1 = Path(str(fn.absolute()))
        #with open(p1, 'rb') as con1:
            #img_bytes = con1.read()
        #img1 = PIL.Image.frombytes('RGB', size,img_bytes)
        #img1.save('/home/user/Downloads/mi1.png')
        #time.sleep(10)
        #print("saved con to")
        #time.sleep(10)
        #print(str(fn.absolute()))
        #snapshot.color_image.data = str(fn.absolute())
        #print(f'now data is {snapshot.color_image.data}')
        #print(snapshot.pose)
        #print(snapshot.feelings)
        #print("*********************************************************")
        m = MessageToJson(snapshot)
        #_snapJ = json.loads(MessageToJson(snapshot))
        colorPath = f'"colorPath": "{str(fn.absolute())}"'
        #print(colorPath)
        userAndSnap = user[:-1] +',' + colorPath+ ',' +m[1:]
        print(userAndSnap[0:250])
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
