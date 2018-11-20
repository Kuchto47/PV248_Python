import sys
import http.server
import http.client


PORT = int(sys.argv[1])
HOST = sys.argv[2]


class MyHandler(http.server.BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()

    def do_GET(self):
        self.set_headers()
        print("Hello biatch from GET")

    def do_POST(self):
        self.set_headers()
        print("Hello biatch from POST")


server = http.server.HTTPServer(("", PORT), MyHandler)
print("serving at port", PORT)
server.serve_forever()
