import binascii
import hashlib
import os
import csv
import io

def makeDigestAuthChallenge(realm):
    # Calculate the digest parameters
    comps = {}
    comps['realm'] = realm
    comps['opaque'] = binascii.hexlify(os.urandom(16))
    comps['nonce'] = hashlib.md5(comps['opaque']).hexdigest()

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

def testDigestAuthResponse(realm, digest, usercreds, verb='GET'):
    try:
        # Make sure the digest starts properly
        if not digest.startswith('Digest '):
            return False

        # Remove the digest leadin
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

        # Make sure the fields we are going to look at are in the digest
        if  'opaque'    not in digestDict or \
            'realm'     not in digestDict or \
            'username'  not in digestDict or \
            'response'  not in digestDict or \
            'uri'       not in digestDict or \
            'qop'           in digestDict: # Chosen directive requires qop be unset
            return False

        # Make sure the realm is right before going any further
        if digestDict['realm'] != realm:
            return False
        
        # Make sure the username is in our 'database'
        if digestDict['username'] not in usercreds:
            return False
        
        # Calculate a response from the given fields and compare it to the given response
        nonce = hashlib.md5(digestDict['opaque'].encode()).hexdigest()
        correctResponse = makeMD5DigestResponse(digestDict['username'], usercreds[digestDict['username']], realm, verb, digestDict['uri'], nonce)
        print(correctResponse)
        if digestDict['response'] == correctResponse:
            return True
        return False

    except:
        return False

def makeMD5DigestResponse(username, password, realm, verb, uri, nonce):
    # Coded based on http://en.wikipedia.org/wiki/Digest_access_authentication
    HA1 = hashlib.md5((username + ':' + realm + ':' + password).encode()).hexdigest()
    HA2 = hashlib.md5((verb.upper() + ':' + uri).encode()).hexdigest()
    return hashlib.md5((HA1 + ':' + nonce + ':' + HA2).encode()).hexdigest()
