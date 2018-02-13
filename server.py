#!/usr/bin/env python

# Author: Daniel-Florin Dosaru dosarudaniel@gmail.com

# How to run the script:
# sudo ./pyScript.py 8080 # as a web server on 8080 port
# check the webage in a browser accesing 'http://localhost:8080/'
# If you get '[Errno 98] Address already in use' try a different port number

import BaseHTTPServer, sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

port = int(sys.argv[1])

### 
class MyHandler(BaseHTTPRequestHandler):
	def do_POST(s):
		print '----- POST'

	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()


	def do_OPTIONS(s):
		# print "------ OPTIONS"
		s.send_response(200)
		
		s.end_headers()

	def do_GET(s):
		print '------ GET'
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

		s.wfile.write("<html><head><title>Title goes here.</title></head>")
		s.wfile.write("<body><p>This is a test.</p>")
		# If someone went to "http://something.somewhere.net/foo/bar/",
		# then s.path equals "/foo/bar/".
		s.wfile.write("<p>You accessed path: %s</p>" % s.path)
		s.wfile.write("</body></html>")

handler = SimpleHTTPRequestHandler
server = BaseHTTPServer.HTTPServer

server_address = ('127.0.0.1', port)
handler.protocol_version = "HTTP/1.0"
httpd = server(server_address, MyHandler)

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()