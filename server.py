#!/bin/env python
from __future__ import print_function
import sys
import time

# Source: https://github.com/Nakiami/MultithreadedSimpleHTTPServer
try:
    # Python 2.x
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
    from urlparse import urlparse
except ImportError:
    # Python 3.x
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class SlowPostRequestHandler(SimpleHTTPRequestHandler):
  def do_POST(self):

        # Sleep for 5 seconds just to trigger the bug
        time.sleep(5)

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytes("Hello world!", "utf8"))
        return

  def do_GET(self):
        parsedParams =  urlparse(self.path)
        print(parsedParams.path);
        if(parsedParams.path == '/another-page.html'):
            # Sleep for 2 seconds just to trigger the bug
            time.sleep(2)   
        return SimpleHTTPRequestHandler.do_GET(self);

if __name__ == '__main__':
    server = ThreadingSimpleServer(('localhost', 8081), SlowPostRequestHandler)
    print("Starting server on http://localhost:8081/")
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("Finished")
