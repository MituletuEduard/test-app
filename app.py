import http.server
import socketserver
import subprocess
import urllib.parse
import sqlite3
import hashlib

PORT = 8080

# VULNERABILITATE: Hardcoded Secret
API_KEY = "12345-SECRET-KEY-ADMIN"

class VulnerableHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parsăm URL-ul pentru a lua parametrii
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)

        # 1. SQL INJECTION (Fără librării externe)
        if 'user' in params:
            user_input = params['user'][0]
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            # Vulnerabil: Concatenare directă
            query = "SELECT * FROM users WHERE name = '" + user_input + "'"
            cursor.executescript(query) # executescript e foarte periculos
            conn.close()

        # 2. COMMAND INJECTION
        if 'cmd' in params:
            cmd_input = params['cmd'][0]
            # Vulnerabil: Execută orice comandă de sistem
            subprocess.call(cmd_input, shell=True)

        # 3. WEAK CRYPTO
        if 'pass' in params:
            pass_input = params['pass'][0]
            # Vulnerabil: MD5
            h = hashlib.md5(pass_input.encode()).hexdigest()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Server Vulnerabil Ruland...")

# Pornim serverul
if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), VulnerableHandler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()
