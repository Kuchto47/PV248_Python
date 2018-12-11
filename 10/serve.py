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

    def set_headers(self, code, path_to_file, reason=None):
        if reason is not None:
            self.send_error(code, explain=reason)
            self.end_headers()
        else:
            self.send_response(code)
            if path_to_file.endswith(".txt"):
                self.send_header("Content-Type", "text/plain")
            else:
                self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", os.path.getsize(path_to_file))
            self.send_header("Content-Disposition", 'attachment; filename="' + os.path.basename(path_to_file) + "\"")
            self.end_headers()

    def do_GET(self):
        self.deal_with_request()

    def do_POST(self):
        self.deal_with_request()

    def deal_with_request(self):
        relative_path = self.path[1:]
        file_name, cgi_params = self.get_request_params(relative_path)
        path_to_file = os.path.join(DIR, file_name)
        if os.path.isfile(path_to_file):
            if path_to_file.endswith(".cgi"):
                self.start_cgi(path_to_file, cgi_params)
            else:
                self.serve_static_content(path_to_file)
        elif os.path.isdir(path_to_file):
            self.set_headers(403, "Forbidden - Requested path is a directory")
        else:
            self.set_headers(404, "Not found")

    def get_request_params(self, relative_path):
        splitted = relative_path.split("?")
        if len(splitted) == 1:
            return splitted[0], None
        else:
            return splitted[0], splitted[1]

    def start_cgi(self, path_to_file, cgi_params):
        path_to_cgi_relative_to_current = os.path.relpath(path_to_file)
        actual_cgi = os.path.basename(path_to_cgi_relative_to_current)
        if cgi_params is not None:
            actual_cgi += "?" + cgi_params
        self.cgi_info = os.path.dirname(path_to_cgi_relative_to_current), actual_cgi
        self.run_cgi()

    def serve_static_content(self, path_to_file):
        self.set_headers(200, path_to_file)
        with open(path_to_file, 'rb') as f:
            while True:
                chunk = f.read(256)
                if not chunk:
                    break
                self.wfile.write(chunk)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


server = Server(("", PORT), ServerHandler)
print("serving at port", PORT, "DIR:", DIR)
server.serve_forever()
