import sys
import http.server
import http.client
import json
import socket


PORT = int(sys.argv[1])


def parse_url(url):
    index = url.find("//")
    if index == -1:
        split_index = url.find("/")
        if split_index == -1:
            return url, ""
    else:
        split_index = url[index+2:].find("/")
        if split_index == -1:
            return url[index+2:], ""
        else:
            split_index += index + 2
    return url[index+2 if index > 0 else 0:split_index], url[split_index:]


def check_json(post_json):
    if "type" in post_json and post_json["type"] == "POST" and ("url" not in post_json or "content" not in post_json):
        return False, None, None, None, None, None
    m_type = post_json["type"] if "type" in post_json else "GET"
    m_url = parse_url(post_json["url"] if "url" in post_json else str(sys.argv[2]))
    m_headers = post_json["headers"] if "headers" in post_json else {}
    m_content = None if m_type == "GET" else post_json["content"]
    m_timeout = post_json["timeout"] if "timeout" in post_json else 1
    return True, m_type, m_url, m_headers, m_content, m_timeout


class ServerHandler(http.server.BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        parsed_url = parse_url(str(sys.argv[2]))
        client = http.client.HTTPConnection(parsed_url[0], timeout=1)
        header = self.headers  # {"Content-Type": "application/json"}
        timeout = True
        try:
            client.request('GET', parsed_url[1], headers=header)
            timeout = False
        except socket.timeout:
            pass
        response = client.getresponse()
        self.set_headers()
        self.construct_json(response, timeout)

    def do_POST(self):
        try:
            post_json = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))).decode())
            result = check_json(post_json)
            if result[0] is False:
                self.set_headers()
                self.construct_json(response=None, timeout=False, invalid_json=True)
            else:
                client = http.client.HTTPConnection(result[2][0], timeout=result[5])
                try:
                    client.request(result[1], result[2][1], headers=result[3], body=result[4])
                    self.set_headers()
                    self.construct_json(client.getresponse(), False)
                except socket.timeout:
                    self.set_headers()
                    self.construct_json(None, True)
        except ValueError:
            self.set_headers()
            self.construct_json(None, False, True)

    def construct_json(self, response, timeout, invalid_json=False):
        d = {}
        if timeout is True:
            code = "timeout"
        elif invalid_json is True:
            code = "invalid json"
        else:
            code = response.getcode()
        d["code"] = code
        if timeout is True or invalid_json is True:
            self.return_json(d)
        else:
            body = response.read()
            try:
                response_body = json.loads(body.decode())
                d["json"] = response_body
            except ValueError:
                pass
            d["headers"] = response.getheaders()
            if "json" not in d.keys():
                d["content"] = str(body)
            self.return_json(d)

    def return_json(self, d):
        self.wfile.write(bytes(json.dumps(d, indent=4, ensure_ascii=False).encode()))


server = http.server.HTTPServer(("", PORT), ServerHandler)
print("serving at port", PORT)
server.serve_forever()
