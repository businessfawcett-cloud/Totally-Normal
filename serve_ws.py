"""
serve_ws.py - Runs a Whitespace program and serves its output as a website.

The WS program should output HTML. This server runs it once at startup
and serves the result on http://localhost:8080.

It also provides /source to inspect the invisible bytes.
"""

import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Import the Whitespace interpreter from run_ws.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_ws import load_program, tokenize, run


class WhitespaceHandler(BaseHTTPRequestHandler):
    ws_output = ""
    ws_bytes = []

    def do_GET(self):
        path = urlparse(self.path).path

        if path == '/source':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'bytes': self.ws_bytes}).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.ws_output.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"  {args[0]}")


def main():
    ws_file = sys.argv[1] if len(sys.argv) > 1 else 'site.ws'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080

    if not os.path.exists(ws_file):
        print(f"Error: {ws_file} not found.")
        print(f"Run: python text_to_ws.py site.html {ws_file}")
        sys.exit(1)

    print(f"Loading {ws_file}...")
    program = load_program(ws_file)
    tokens = tokenize(program)

    print("Executing Whitespace program...")
    output = run(tokens)
    WhitespaceHandler.ws_output = output
    WhitespaceHandler.ws_bytes = [ord(c) for c in program]

    print(f"Output: {len(output)} bytes of HTML")
    print(f"Source: {len(program)} whitespace bytes (0 visible characters)")
    print(f"\nServing at http://localhost:{port}")
    print("Press Ctrl+C to stop.\n")

    server = HTTPServer(('0.0.0.0', port), WhitespaceHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == '__main__':
    main()
