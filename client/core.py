import argparse
import socket
from urllib.parse import urlparse
import httputil
from getpass import getpass

def makeRequest(host, resource, verb='GET', extraHeaders={}):
    lines = []
    lines.append(verb + ' ' + resource + ' HTTP/1.0')
    lines.append('Host: ' + host)
    for key in extraHeaders:
        lines.append(key + ': ' + extraHeaders[key])
    lines.append('\r\n')
    return '\r\n'.join(lines)

def parseArgs():
    #Perform argument parsing
    parser = argparse.ArgumentParser(description="Send get request to server")
    parser.add_argument('url', help="URL of destination")
    parser.add_argument('port', type=int, help="Port number of destination")   
    return parser.parse_args()
    
def runClient(target, port):
    #parse target url
    o = urlparse(target)
    if o.netloc == '':
        target = 'http://' + target
        o = urlparse(target)
    resource = o.path
    if resource == '':
        resource = '/'
    
    #make socket
    mysocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)    
    #connects socket of input port number to input url
    mysocket.connect((o.netloc, port))        
    
    #send get request
    tosend = makeRequest(o.netloc, resource)  
    mysocket.sendall(tosend.encode())                         
    #receive response from server using socket     
    response = httputil.handleHTTP(mysocket)      
        
    #in the case of authentication
    
    user = input('Username: ')
    spec = getpass('Password: ')
    
 
    #print the response from server  
    mysocket.close()      
    print(response['raw'])       


if __name__ == "__main__":
    commands=parseArgs()
    
    # Print out some basic debug information
    print("Target: " + commands.url)
    print("Port: " + str(commands.port))
    
   # try:
        
    runClient(commands.url, commands.port)
   # except: 
    #    print("Something went wrong!")
