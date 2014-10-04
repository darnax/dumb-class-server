import argparse
import threading
import socketserver
from .dumbserver import hi

class HTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class HTTPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass

def parseArgs():
    parser = argparse.ArgumentParser(description='A basic server')
    parser.add_argument('root', help='The root directory of the server')
    parser.add_argument('port', type=int, help='The port to bind the server to')
    return parser.parse_args()

def startServer(host, port, root):
    server = HTTPServer((host, port), HTTPRequestHandler)
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.start()
    return server, serverThread

if __name__ == "__main__":
    params = parseArgs()
    server, serverThread = startServer('localhost', params.port, params.root)
    print("Server started")
    try:
        serverThread.join()
    except KeyboardInterrupt:
        print("Warm shutdown...")
        server.shutdown()
        try:
            serverThread.join()
        except KeyboardInterrupt:
            print("Cold shutdown...")
