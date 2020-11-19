#!/usr/local/bin/python3

# Web server to respond with 302 - plus verbose logging to stdout

#!/usr/bin/env python3
'''
Usage::
    ./redir.py [<port>] [<redirect-host>]
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import parse_headers
import logging
import sys

class S(BaseHTTPRequestHandler):
    def _set_response_redir(self):
        if len(sys.argv) > 2:
            if sys.argv[2]:
                redir_location = sys.argv[2]
        else:
            redir_location = 'http://localhost'
        self.send_response(302)
        self.send_header('Location', redir_location)
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        headers = str(self.headers)
        self._set_response_redir()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response_redir()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) >= 2:
        run(port=int(argv[1]))
    else:
        run()
