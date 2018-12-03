import sys
import http.server
import socketserver
import os
import cgi


PORT = int(sys.argv[1])
DIR = str(sys.argv[2])


class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        relative_path = self.requestline.split(" ")[1][1:]
        path_to_file = os.path.join(DIR, relative_path)
        file_extension = os.path.splitext(path_to_file)[1]
        if file_extension == ".cgi":
            
            # file = open(path_to_file, 'rb').read()
            # self.set_headers()
            # self.wfile.write(bytes(file))
            pass
        else:
            super().do_GET()

    def do_POST(self):
        self.set_headers()


server = socketserver.TCPServer(("", PORT), ServerHandler)
print("serving at port", PORT, "DIR:", DIR)
server.serve_forever()
