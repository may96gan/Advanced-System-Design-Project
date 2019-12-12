#!/usr/bin/python
import functools
from http.server import BaseHTTPRequestHandler
import http.server
import re


class Website:

    handlers = {}

    def route(self, path):
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            self.handlers[path] = f
            return wrapper
        return decorator

    def run(self, address):
        ws = self

        class MyHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                func = None
                func_args = ""
                for k in ws.handlers.keys():
                    r = re.match(fr"^{k}$", self.path)
                    if r:
                        if k != '/':
                            func_args = r.group(1)
                        func = ws.handlers[k]
                if func is None:
                    self.send_response(404)
                    self.end_headers()
                else:
                    status_code, body = func(*func_args)
                    self.send_response(status_code)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bytes(body, 'UTF-8'))
        http_server = http.server.HTTPServer((address), MyHandler)
        http_server.serve_forever()
