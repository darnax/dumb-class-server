import argparse
import socketserver
import os
import os.path

# local imports
import httputil
import digestauth
from responsemap import ResponseMap

authrealm = 'Magical Digestion'
usercreds = {
    'darnax': 'stinky',
    'magic': 'worlds'
}

class HTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

class HTTPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        response = None
        try:
            # Parse the request then send back a respone
            requestData = httputil.handleHTTP(self.request)
            print("Request Received:")
            print(requestData['raw'])
            response = makeFileResponse(self.server.httpRoot, requestData)
        except:
            response = makeHTTPResponse(400)

        print("Sending Response:")
        print(response.decode())
        self.request.sendall(response)

def makeFileResponse(root, request):
    # Determine the path of the file we are looking for
    filePath = safeJoin(root, request['resource'])

    # Make sure the file exists (give back a 404 if it does not)
    if os.path.isfile(filePath):
        # Perform an auth step if it is in the protected sub-directory
        if filePath.startswith(root + '/protected/') and \
        ('Authorization' not in request['headers'] or \
        not digestauth.testDigestAuthResponse(authrealm, request['headers']['Authorization'], usercreds)):
            return makeHTTPResponse(401, headers={'WWW-Authenticate': digestauth.makeDigestAuthChallenge(authrealm)})

        # Open and read the file to send back a response
        with open(filePath, 'r') as f:
            return makeHTTPResponse(200, payload=f.read())
    return makeHTTPResponse(404)

def makeHTTPResponse(code, headers={}, payload=''):
    # Make sure we actually know the name for this code
    if code not in ResponseMap:
        raise LookupError(code + ' not found in supported response codes')

    # Insert required parts of response
    response = []
    response += 'HTTP/1.0 ' + str(code) + ' ' + ResponseMap[code] + '\r\n'
    response += 'Content-Length: ' + str(len(payload)) + '\r\n'

    # Insert any extrea headers given
    for key in headers:
        response += key + ': ' + headers[key] + '\r\n'

    # End the response with a blank line and the payload
    response += '\r\n'
    response += payload
    return ''.join(response).encode('ascii')

def safeJoin(base, resource):
    # Needed a function to prevent path joins from using /../ or anything similar to access illegal locations
    # (I once had to help a community recover from the effects of a hack caused by this very issue -Chris)
    # Referenced http://stackoverflow.com/questions/1950069/suspicious-operation-django for this function
    # Security is very important and should always be crowdsourced when possible
    base = os.path.normcase(os.path.abspath(base))
    result = os.path.normcase(os.path.abspath(base + resource))
    baselen = len(base)
    if not result.startswith(base) or result[baselen:baselen+1] not in ('', os.sep):
        raise ValueError('The joined path is outside of the base path')

    return result

def parseArgs():
    # Perform argument parsing
    parser = argparse.ArgumentParser(description='A basic server')
    parser.add_argument('root', help='The root directory of the server')
    parser.add_argument('port', type=int, help='The port to bind the server to')
    return parser.parse_args()

def runServer(host, port, root):
    # Make sure the given root is valid
    if not os.path.exists(root):
        print("Root path not found")
        return
    if not os.path.isdir(root):
        print("Root path is not a directory")
        return
    root = os.path.normcase(os.path.abspath(root))

    # Start up the server
    server = HTTPServer((host, port), HTTPRequestHandler)
    server.httpRoot = root

    # Print out some basic debug information
    print("Host: " + host)
    print("Port: " + str(port))
    print("Base directory: " + root)

    # Enter an endless multi-threaded loop
    server.serve_forever()

if __name__ == "__main__":
    params = parseArgs()
    print("Running server")
    try:
        runServer('0.0.0.0', params.port, params.root)
    except KeyboardInterrupt:
        print("Server shutdown")