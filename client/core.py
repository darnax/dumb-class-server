import argparse
import socket
from urllib.parse import urlparse
import httputil
from getpass import getpass
import os
import csv 
import io
import hashlib

def makeRequest(host, resource, verb='GET', extraHeaders={}):
    # creates a GET request 
    lines = []
    lines.append(verb + ' ' + resource + ' HTTP/1.0')
    lines.append('Host: ' + host)
    for key in extraHeaders:
        lines.append(key + ': ' + extraHeaders[key])
    lines.append('\r\n')
    return '\r\n'.join(lines)

def parseArgs():
    # Perform argument parsing
    parser = argparse.ArgumentParser(description="Send get request to server")
    parser.add_argument('url', help="URL of destination")
    parser.add_argument('port', type=int, help="Port number of destination")   
    return parser.parse_args()
    
def makeMD5DigestResponse(username, password, realm, verb, uri, nonce):
    # Coded based on http://en.wikipedia.org/wiki/Digest_access_authentication
    HA1 = hashlib.md5((username + ':' + realm + ':' + password).encode()).hexdigest()
    HA2 = hashlib.md5((verb.upper() + ':' + uri).encode()).hexdigest()
    return hashlib.md5((HA1 + ':' + nonce + ':' + HA2).encode()).hexdigest()

def makeDigestAuthChallenge(user, password, uri, response):
    # obtain digest from response message
    digest = response['headers']['WWW-Authenticate']
    digest = digest[7:]
    
    # Process the digest into a dictionary (its basically CSV with key-values)
    csvReader = csv.reader(io.StringIO(digest))
    fields = []
    digestDict = {}
    for row in csvReader:
        fields.extend(row)
    for field in fields:
        parts = field.strip().split('=', 1)
        if len(parts) != 2:
            return False
        if not parts[1].startswith('"') or not parts[1].endswith('"'):
            return False
        digestDict[parts[0]] = parts[1][1:-1]

    # Calculate the digest parameters
    comps = {}
    comps['username'] = user
    comps['realm'] = digestDict['realm']
    comps['uri'] = uri
    comps['opaque'] = digestDict['opaque']
    comps['nonce'] = digestDict['nonce']
    comps['response'] = makeMD5DigestResponse(user, password, digestDict['realm'], 'GET', uri, comps['nonce'])
    # Build the digest
    parts = ['Digest ']
    for key in comps:
        if type(comps[key]) == type(b''):
            comps[key] = comps[key].decode()
        parts += key + '="' + comps[key] + '",'

    # Remove trailing comma
    parts[len(parts)-1] = parts[len(parts)-1][:-1]

    # Perform fast string concatenation to create the result
    return ''.join(parts)
    
    
def runClient(target, port):
    # parse target url
    o = urlparse(target)
    if o.netloc == '':
        target = 'http://' + target
        o = urlparse(target)
    resource = o.path
    if resource == '':
        resource = '/' 
    
    # make socket
    mysocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)    
    # connects socket of input port number to input url
    mysocket.connect((o.netloc, port))        
    
    # send initial GET request
    tosend = makeRequest(o.netloc, resource)  
    mysocket.sendall(tosend.encode())                         
    # receive response from server using socket     
    response = httputil.handleHTTP(mysocket)          
    mysocket.close()
    
    # in the case of authentication, input username and password
    if 'WWW-Authenticate' in response['headers']:
        user = input('Username: ')
        spec = getpass('Password: ')
        sDigest = makeDigestAuthChallenge(user, spec, resource, response)
        valid = makeRequest(o.netloc, resource, 'GET', extraHeaders = {'Authorization': sDigest})
        # create second socket and send get request with authorization data
        secondsocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)    
        secondsocket.connect((o.netloc, port))     
        secondsocket.sendall(valid.encode())
        response = httputil.handleHTTP(secondsocket)  
        secondsocket.close()
 
    # print the response from server      
    print(response['raw'])       


if __name__ == "__main__":
    commands=parseArgs()
    
    # Print out some basic information
    print("Target: " + commands.url)
    print("Port: " + str(commands.port))
    
    #run the client    
    runClient(commands.url, commands.port)
