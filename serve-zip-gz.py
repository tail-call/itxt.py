#!/usr/bin/env python3
import time
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from zipfile import ZipFile
from sys import argv

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

filename = argv[1]
source = ZipFile(filename, 'r')

class Server(BaseHTTPRequestHandler):
    # def do_HEAD(self):
    #     return
    # def do_POST(self):
    #     return
    def handle_404(self, path):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        body = '''
        404: {} not found. See <a href="/.list">full index</a>
        '''.format(path)
        self.wfile.write(bytearray(body, 'utf-8'))
    def serve_list(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        body = '<br>\n'.join(['<a href="/{0}">{0}</a>'.format(name) for name in source.namelist()])
        self.wfile.write(bytearray(body, 'utf-8'))
    def do_GET(self):
        if self.path == '/.list':
            return self.serve_list()

        path = self.path[1:]
        if self.path == '/':
            path = 'index.html'

        try:
            with source.open(path) as output:
                self.send_response(200)
                self.send_header('Content-Encoding', 'gzip')
                self.end_headers()
                self.wfile.write(output.read())
        except KeyError:
            self.handle_404(path)

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print('Open http://{}:{} in your browser to browse {}'.format(HOST_NAME, PORT_NUMBER, filename))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
