#!/usr/bin/env python3
"""
Local development server with manifest editing support.
Serves static files and provides a POST endpoint to save manifest.json.

Usage: python3 editor-server.py
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8000
MANIFEST_PATH = os.path.join('assets', 'manifest.json')


class EditorHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/api/save-manifest':
            self._save_manifest()
        else:
            self.send_error(404, 'Not Found')

    def _save_manifest(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            # Validate basic structure
            if 'models' not in data or not isinstance(data['models'], list):
                self.send_error(400, 'Invalid manifest: missing "models" array')
                return

            # Pretty-print to keep the file readable
            with open(MANIFEST_PATH, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'ok': True,
                'models': len(data['models'])
            }).encode())
            print(f"✅ Manifest saved — {len(data['models'])} models")

        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON')
        except Exception as e:
            self.send_error(500, str(e))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        if self.path and self.path.startswith('/sw.js'):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or '.')
    server = HTTPServer(('', PORT), EditorHandler)
    print(f"🚀 Editor server running at http://localhost:{PORT}")
    print(f"📝 Editor UI:  http://localhost:{PORT}/editor.html")
    print(f"📁 Manifest:   {os.path.abspath(MANIFEST_PATH)}")
    print(f"   Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
