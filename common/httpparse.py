
def parseRequest(rawRequest):
    pass

def parseResponse(rawResponse):
    pass

def makeRequest(host, resource, verb='GET', extraHeaders={}):
    lines = []
    lines.append(verb + ' ' + resource + ' HTTP/1.0')
    lines.append('Host: ' + host)
    for key in extraHeaders:
        lines.append(key + ': ' + extraHeaders[key])
    return '\r\n'.join(lines)

def makeResponse(code, headers, data):
    pass