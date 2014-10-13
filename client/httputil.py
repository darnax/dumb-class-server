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
    data['raw'] += line

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

    lastheader = None
    while line != '\r\n':
        line, extra = recv_until(sock, '\r\n', extra, buff)
        data['raw'] += line
        
        # Try to parse the header if possible
        if line.startswith(' '):
            data['headers'][lastheader] += line[:-2]
        else:
            parts = line.split(': ', 1)
            if len(parts) == 2:
                lastheader = parts[0]
                data['headers'][parts[0]] = parts[1][:-2]

    # Check if a body should be present
    if 'Content-Length' in data['headers']:
        clength = int(data['headers']['Content-Length']) - len(extra)
        data['body'] = extra
        if clength > 0:
            data['body'] += sock.recv(clength).decode()
        
        data['raw'] += data['body']

    # Merge the response fields
    data['raw'] = ''.join(data['raw'])
    return data