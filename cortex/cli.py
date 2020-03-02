#!/usr/bin/python

import datetime
import click 
import json
import requests

@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback

@main.command('get-users')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
def get_users(host, port):
    _url = f'http://{host}:{port}/users'
    result = requests.get(_url).json()['currentUsers']
    if result:
        print('Users:')
        for u in result:
            print(f"User id is {u['user_id']}, user name is {u['username']}")
        else:
            print('No users.')

@main.command('get-user')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('user_id', type=int)
def get_user(host, port, user_id):
    _url = f'http://{host}:{port}/users/{user_id}'
    result = requests.get(_url)
    if result.status_code == 404:
        print(result.text)
    elif result.status_code == 200:
        u = result.json()
        print(f"User id is {u['user_id']}, user name is {u['username']}")
        print(f"User's birthday is {datetime.datetime.fromtimestamp(u['birthday']/1000)}")
        g = u['gender']
        if g == 0:
            print("User's gender: male")
        elif g == 1:
            print("User's gender: female")

@main.command('get-snapshots')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('user_id', type=int)
def get_snapshots(host, port, user_id):
    _url = f'http://{host}:{port}/users/{user_id}/snapshots'
    result = requests.get(_url)
    if result.status_code == 404:
        print(result.text)
    elif result.status_code == 200:
        u = result.json()['currentSnapshots']
        if ss:
            print("User's Snapshots:")
            for s in ss:
                print(f"Snapshot id is {s['_id']}, datetime: {datetime.datetime.fromtimestamp(s['datetime']/1000)}")
        else:
            print("No snapshots of this user.")

@main.command('get-snapshot')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=str)
def get_snapshot(host, port, user_id, snapshot_id):
    _url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    result = requests.get(_url)
    if result.status_code == 404:
        print(result.text)
    elif result.status_code == 200:
        s = result.json()
        print(f"Snapshot id is {s['_id']}, datetime: {datetime.datetime.fromtimestamp(s['datetime']/1000)}")
        print(f"Available results for this snapshot are: {s['results']}")

@main.command('get-result')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=str)
@click.argument('result', type=str)
def get_result(host, port, user_id, snapshot_id,result):
    _url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result}'
    result = requests.get(_url)
    if result.status_code == 404:
        print(result.text)
    elif result.status_code == 200:
        s = result.json()
        print(f"Snapshot {result}:")
        print(s)






if __name__ == '__main__':
    main()
    print('done')
