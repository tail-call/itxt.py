from sys import argv
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

filename = argv[1]

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/png')
        self.send_header('Content-Encoding', 'gzip')
        self.end_headers()
        with open(filename, mode='rb') as input:
            self.wfile.write(b'\x1f\x8b\x08\x00\x00\x00\x00\x00' + input.read())

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print('Open http://{}:{} in your browser to browse {}'.format(HOST_NAME, PORT_NUMBER, filename))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
