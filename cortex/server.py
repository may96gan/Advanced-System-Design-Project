#!/usr/bin/python
from pathlib import Path as path
import struct
from datetime import datetime
import threading
from flask import Flask
from flask import request
import pika
import click

@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass


def run_server(host, port, publish):
    publish = publish
    
    app = Flask(__name__)

    @app.route('/config', methods = ['GET'])
    def myParsers():
        print("in server parsers")
        return "hello parsers"

    @app.route('/snapshot', methods = ['POST'])
    def newSnapshot():
        print("in server snapshot")
        snapshot = request.get_data()
        publish(snapshot)
        print("done")
        return "ok"
        

    app.run(host = host,port = port,threaded=True)

@main.command('run-server')
@click.option('-h','--host', default='127.0.0.1')
@click.option('-p','--port', default=8000)
@click.argument('publish', default='rabbitmq://127.0.0.1:5672/')
def run_server_cli(host,port,publish):
    connection = pika.BlockingConnection(pika.ConnectionParameters(publish))
    channel = connection.channel()
    channel.exchange_declare(exchange='snapshots',exchange_type='fanout')
    def mq_publish(snapshot):
        channel.basic_publish(exchange='snapshots',
                              routing_key='',
                              body=snapshot)
    #channel.queue_declare(queue='current_snapshots')
    run_server(host,port,mq_publish)

if __name__ == '__main__':
    main()
