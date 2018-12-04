import sys
import http.server
import socketserver
import os


PORT = int(sys.argv[1])
DIR = str(sys.argv[2])


class ServerHandler(http.server.CGIHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    cgi_directories = [DIR]

    def set_headers(self, code, reason=None):
        if reason is not None:
            self.send_error(code, explain=reason)
        else:
            self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        self.deal_with_request()

    def do_POST(self):
        self.deal_with_request()

    def deal_with_request(self):
        relative_path = self.path[1:]
        path_to_file = os.path.join(DIR, relative_path)
        if os.path.isfile(path_to_file):
            file_extension = os.path.splitext(path_to_file)[1]
            if file_extension.lower() == ".cgi":
                dir_without_slash = DIR if (not DIR.endswith('/') and not DIR.endswith('\\')) else DIR[:-1]
                self.cgi_info = dir_without_slash, relative_path
                self.run_cgi()
            else:
                super().do_GET()
            # file = open(path_to_file, 'rb').read()
            # self.set_headers()
            # self.wfile.write(bytes(file))
            pass
        elif os.path.isdir(path_to_file):
            self.set_headers(403, "Forbidden - Requested path is a directory")
        else:
            self.set_headers(404, "Not found")


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


server = Server(("", PORT), ServerHandler)
print("serving at port", PORT, "DIR:", DIR)
server.serve_forever()
