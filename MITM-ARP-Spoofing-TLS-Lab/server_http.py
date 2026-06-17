#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse, sys, os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/form.html':
            try:
                with open('form.html','rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type','text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8', errors='ignore')
        parsed = urllib.parse.parse_qs(body)
        log_line = "=== RECEIVED FORM ===\\n" + body + "\\n" + str(parsed) + "\\n"
        sys.stderr.write(log_line)
        with open('last_post.log','a') as logfile:
            logfile.write(log_line)
        self.send_response(200)
        self.send_header('Content-type','text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Thanks. Form received.\\n")

if _name_ == '_main_':
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    print("Serving on 0.0.0.0:8080", file=sys.stderr)
    server.serve_forever()
PY