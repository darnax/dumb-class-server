import argparse
import threading
import socketserver

class HTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class HTTPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            request = handleHTTP(self.request)
            print(request)
        except IOError as ex:
            print("Malformed Request: " + str(ex))

# Optimized for short lines
def recv_until(sock, until, overflow='', scratchSpace=bytearray(1024)):
    line = overflow
    end = line.find(until)

    while end == -1:
        byteCount = sock.recv_into(scratchSpace)
        if byteCount == 0:
            raise IOError("Socket closed")
        line += scratchSpace[0:byteCount].decode()
        end = line.find(until)
    end += len(until)

    return line[0:end], line[end:]

def handleHTTP(sock):
    # Initialize read buffer
    buff = bytearray(1024)

    # Initialize parse structure
    data = {}
    data['headers'] = {}
    data['raw'] = [] # Join at the end to prevent wasting time on new allocations

    # Receive and parse the initial line
    extra = ''
    line, extra = recv_until(sock, '\r\n', extra, buff)
    data['raw'].append(line)

    # Break down the line into parts
    parts = line.split(' ', 2)
    if len(parts) != 3:
        raise IOError("Malformed HTTP data")
    parts[2] = parts[2][:-2] # Remove the trailing \r\n

    # Determine if this is a request or a response
    if len(parts[0]) > 4 and parts[0][0:4] == 'HTTP':
        data['type'] = 'response'
        data['version'] = parts[0]
        try:
            data['code'] = int(parts[1])
        except ValueError:
            raise IOError("Malformed HTTP response code")
        data['codestr'] = parts[2]
    else:
        data['type'] = 'request'
        data['verb'] = parts[0]
        data['resource'] = parts[1]
        data['version'] = parts[2]

    while line != '\r\n':
        line, extra = recv_until(sock, '\r\n', extra, buff)
        data['raw'].append(line)
        
        # Try to parse the header if possible
        parts = line.split(': ', 1)
        if len(parts) == 2:
            data['headers'][parts[0]] = parts[1][:-2]    

    # Check if a body should be present
    if 'Content-Length' in data['headers']:
        clength = int(data['headers']['Content-Length']) - len(extra)
        data['body'] = extra
        if clength > 0:
            data['body'] += sock.recv(clength)
        
        data['raw'].append(data['body'])

    # Merge the response fields
    data['raw'] = ''.join(data['raw'])
    return data

def parseArgs():
    parser = argparse.ArgumentParser(description='A basic server')
    parser.add_argument('root', help='The root directory of the server')
    parser.add_argument('port', type=int, help='The port to bind the server to')
    return parser.parse_args()

def runServer(host, port, root):
    server = HTTPServer((host, port), HTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    params = parseArgs()
    print("Running server")
    try:
        runServer('0.0.0.0', params.port, params.root)
    except KeyboardInterrupt:
        print("Server shutdown")