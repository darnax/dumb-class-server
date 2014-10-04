import argparse
import socket

def parseArgs():
    parser = argparse.ArgumentParser(description="Send get request to server")
    parser.add_argument('url', help="URL of destination")
    parser.add_argument('port', type=int, help="Port number of destination")   
    return parser.parse_args()

if __name__ == "__main__":
    commands=parseArgs()
    
    mysocket = socket.socket(family=AF_INET, type=SOCK_STREAM)
    
    try:
        mysocket.connect((commands.url, commands.port))       #connects socket of input port number to input url 
        mysocket.send("GET")                                       #send get request
        
        response = mysocket.rcv(1024)      #recieve response from server using socket
        
        if(repr(response) ==  )        #in the case of authentication
            pause
            print(repr(response))       #prints response from server then ask for authentication
            
            mysocket.send()             #send authentication to server
        
        mysocket.close()            #close the socket when finished
        print(repr(response))       #print the response from server