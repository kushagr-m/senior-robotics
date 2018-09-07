from http.server import BaseHTTPRequestHandler,HTTPServer
import threading

PORT = 8000

HTML_DATA = ""
HTML_DATA +=  "<style>input { width: 100%; height: 20% }</style>"
HTML_DATA += "<form action='/start'><input type='submit' value='Start' /></form>"
HTML_DATA += "<form action='/stop'><input type='submit' value='Stop' /></form>"

running = False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global running
        if self.path == "/start?":
            print("Web: start running")
            running = True
        if self.path == "/stop?":
            print("Web: stop running")
            running = False

        status =  "<div>Running: " + str(running) + "</div>"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write((status + HTML_DATA).encode('utf-8'))
        return

def start():
    def start_server():
        try:
            server = HTTPServer(('', PORT), handler)
            print('Started web server on port ' , PORT)
            server.serve_forever()

        except KeyboardInterrupt:
            print('Stopping web server')
            server.socket.close()

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

def is_running():
    return running