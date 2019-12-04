#!/usr/bin/python
from http.server import BaseHTTPRequestHandler
import http.server
from pathlib import Path
import signal


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.respond({'status': 200})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print(path)
        _INDEX_HTML = '''
        <html><head><title>Brain Computer Interface</title></head>
        <body><ul>{users}</ul></body>
        </html>
        '''
        _USER_LINE_HTML = '''
        <li><a href="/users/{user_id}">user {user_id}</a></li>
        '''
        _USER_HTML = '''
        <html><head><title>Brain Computer Interface: User {user_id}
        </title></head>
        <body><table>{thoughts}</table></body>
        </html>
        '''
        _THOUGHT_LINE_HTML = '''
        <tr><td>{date} {time}</td><td>{thought}</td></tr>
        '''
        all_users = []
        users_html = []
        thoughts_html = []
        for user_dir in self.server.data_dir.iterdir():
            users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
            all_users.append("/users/{id}".format(id=user_dir.name))
        index_html = _INDEX_HTML.format(users='\n'.join(users_html))
        if path in all_users:
            cur_user_id = path.split('/')[-1]
            user_path = self.server.data_dir / cur_user_id
            for user_file in user_path.iterdir():
                file_path = Path(user_path / user_file.name)
                file_name = Path(user_file.name).stem
                t_date = file_name.split('_')[0]
                t_time = file_name.split('_')[1].replace('-', ':')
                t = file_path.read_text()
                thoughts_html.append(
                                     _THOUGHT_LINE_HTML.format(
                                                               date=t_date,
                                                               time=t_time,
                                                               thought=t))
            user_html = _USER_HTML.format(user_id=cur_user_id,
                                          thoughts='\n'.join(thoughts_html))
            return bytes(user_html, 'UTF-8')
        return bytes(index_html, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)


def run_webserver(address, data_dir):
    if (isinstance(address, str)):
        adr = tuple(address.split(":"))
        h = adr[0]
        p = (int)(adr[1])
        address = h, p
    http_server = http.server.HTTPServer((address), MyHandler)
    http_server.data_dir = Path(data_dir)
    http_server.serve_forever()


def signal_handler(sig, frame):
    sys.exit(0)


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address>')
        return 1
    try:
        run_webserver(sys.argv[1], sys.argv[2])
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()

    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
