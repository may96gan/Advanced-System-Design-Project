#!/usr/bin/python
import functools
from inspect import getfullargspec
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import socket 
import http.server
from pathlib import Path
import time
import re

class Website:

    def __init__(self):
        self.handlers = {}

    def route(self, path):
        def decorator(f):
            self.handlers[path] = f
            @functools.wraps(f)
            def wrapper(args, *kwargs):
                return f(args, *kwargs)
            return wrapper
        return decorator

    def run(self, address):
        ws = self
        class MyHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path in ws.handlers:
                    status_code, body = ws.handlers[self.path]()
                    
                else:
                    for k in ws.handlers.keys():
                        r = re.fullmatch(k, self.path)
                        if r:
                            status_code, body = ws.handlers[k](*r.groups())
                            break
                        else:
                            status_code, body = 404, ''
                    self.send_response(status_code)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes(body, 'UTF-8'))
        http_server = http.server.HTTPServer((address), MyHandler)
        http_server.serve_forever()
