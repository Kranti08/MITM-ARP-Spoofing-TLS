#!/usr/bin/env python3
import ssl, sys, os
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

CERTFILE = "cert.pem"
KEYFILE = "key.pem"
PORT = 8443
BIND = "0.0.0.0"

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
        log_line = "=== RECEIVED FORM (HTTPS) ===\\n" + body + "\\n" + str(parsed) + "\\n"
        sys.stderr.write(log_line)
        with open('last_post_https.log','a') as logfile:
            logfile.write(log_line)
        self.send_response(200)
        self.send_header('Content-type','text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"Thanks. HTTPS form received.\\n")

if __name__ == '__main__':
    httpd = HTTPServer((BIND, PORT), Handler)
    # set up TLS context for server
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f"Serving HTTPS on {BIND}:{PORT}", file=sys.stderr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down.", file=sys.stderr)
        httpd.server_close()
PY