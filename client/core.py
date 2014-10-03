import argparse
import socket

def parseArgs():
    parser = argparse.ArgumentParser()      
    parser.add_argument(type=string,type=int, help="send get request to server")   
    return parser.parse_args()

if __name__ == "__main__":
    commands=parseArgs()
    
    mysocket = socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)
    
    