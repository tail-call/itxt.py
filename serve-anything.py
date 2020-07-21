#!/usr/bin/env python3
import time
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from http.client import HTTPConnection
from zipfile import ZipFile
from sys import argv

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path[1:]

        try:
            connection = HTTPConnection('www.python.org')
            response = connection.request('GET', path)
            # connection.send()
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # self.wfile.write(connection.getresponse().read())
            self.wfile.write(b'')
        except KeyError:
            self.handle_404(path)

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print('Open http://{}:{} in your browser to browse'.format(HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
