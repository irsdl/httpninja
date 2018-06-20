#!/usr/bin/python
import re
import socket
import urlparse
import ssl
import urllib
import time

# See HTTPPipelineTest() for a simple usage
# Example:
# RequestObject('POST', 'https://soroush.secproject.com/?q1=q2','var=val',{'cookie':'x=2;r=5','connection':'close','Content-Type': 'application/x-www-form-urlencoded'}, True)
class RequestObject(object):
    url = ''
    _path = ''
    _CRLF = '\r\n'
    qs = ''
    cookie = ''
    body = ''
    headers = None
    autoContentLength = True
    autoHOSTHeader = True
    useAbsolutePath = False
    isSSL = False
    HTTPVersion = ''
    targetName = ''
    targetPort = ''
    targetProtocol = ''
    # The class "constructor" - It's actually an initializer
    def __init__(self, method='GET', url='', body='', headers={}, autoContentLength=True, autoHOSTHeader=True, useAbsolutePath=False, HTTPVersion='HTTP/1.1'):
        self.method = method
        self.url = url
        self.body = body
        self.headers = headers
        self.autoContentLength = autoContentLength
        self.autoHOSTHeader = autoHOSTHeader
        self.useAbsolutePath = useAbsolutePath
        self.HTTPVersion = HTTPVersion
        self._setParams()

    def _setParams(self):
        parsedURL = urlparse.urlparse(self.url)
        # setting the path
        if self.useAbsolutePath == True:
            self._path = self.url
        else:
            self._path = parsedURL.path
            self.qs = parsedURL.query

        if self._path == '':
            self._path = '/'

        # fix the body if it is in dict format
        if isinstance(self.body,dict):
            self.body = urllib.urlencode(self.body)

        # set other necessary parameters
        self.targetName = parsedURL.hostname
        self.targetPort = parsedURL.port
        self.targetProtocol = (parsedURL.scheme).lower()
        if self.targetProtocol == 'https':
            self.isSSL = True
            if self.targetPort == None: self.targetPort = 443
        elif self.targetPort == None:
            self.targetPort = 80

    def rawRequest(self):
        self._setParams()

        #building the raw request
        queryString = ''
        hostHeader = ''
        contentLengthHeader = ''
        incomingHeaders = ''
        if self.autoHOSTHeader:
            hostHeader = self._CRLF + "Host: " + self.targetName + self._CRLF
        if self.headers != None and len(self.headers)>0:
            for key, value in self.headers.iteritems():
                incomingHeaders = incomingHeaders + str(key) + ": " + str(value) + self._CRLF
        if incomingHeaders.endswith(self._CRLF):
            incomingHeaders = incomingHeaders[:-2]
        if self.autoContentLength:
            contentLengthHeader = self._CRLF + "Content-Length: " + str(len(self.body))
        if self.qs != '':
            queryString = '?' + self.qs
        httpdata = self.method + " " + self._path + queryString + " " + self.HTTPVersion + hostHeader + incomingHeaders + \
                   contentLengthHeader + self._CRLF + self._CRLF + self.body

        return httpdata


def SendHTTPRequestBySocket(rawHTTPRequest = '', targetName='127.0.0.1', targetPort=80, isSSL = False, timeout=1,
                            includeTimeoutErr=False, isRateLimited=False, sendInitialChars=0, sendBodyCharRate=1, delayInBetween=0.2):
    if len(rawHTTPRequest) == 0: return

    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if isSSL:
        s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1) # Perhaps this needs to be changed when other protocols should be used

    s.settimeout(timeout)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.connect((targetName, targetPort))

    # s.send(unicode(rawHTTPRequest, 'utf-8'))
    if isRateLimited is False or sendBodyCharRate <= 0 or sendBodyCharRate <= 0 or delayInBetween < 0:
        s.send(rawHTTPRequest)
    else:
        if sendInitialChars > 0:
            s.send(rawHTTPRequest[:sendInitialChars])
            rawHTTPRequest = rawHTTPRequest[sendInitialChars:]

        for i in range(0, len(rawHTTPRequest), sendBodyCharRate):
            time.sleep(delayInBetween)
            s.send(rawHTTPRequest[i:i + sendBodyCharRate])


    response = b''

    while True:
        try:
            buf = s.recv(1024)
            if not buf: break
            response = response + buf
        except socket.timeout, e:
            err = e.args[0]
            if err == 'timed out' and includeTimeoutErr:
                if response != '':
                    response = response + '\nErr: last part was timed out'
                else:
                    response = 'Err: timed out'
            break
    s.close()
    return response

def RequestObjectsToHTTPPipeline(RequestObjects):
    result = ''
    if len(RequestObjects) <= 0: raise ValueError('less_than_two_elements_received_by_RequestObjectsToHTTPPipeline()')
    CRLF = '\r\n'
    mainTarget = ''
    mainPort = ''
    lastElement = True
    for reqObjects in reversed(RequestObjects):
        if mainTarget == '':
            mainTarget = reqObjects.targetName
            mainPort = reqObjects.targetPort
        IsConnectionSet = False
        if reqObjects.headers != None:
            for key, value in reqObjects.headers.iteritems():
                if re.search(r'(connection:\s*close)|(connection:\s*keep\-alive)', str(key) +":" + str(value),
                             flags=re.IGNORECASE) != None:
                    IsConnectionSet = True
                    reqObjects.headers[key] = 'keep-alive'

        if IsConnectionSet == False:
            if lastElement:
                reqObjects.headers['Connection'] = 'close'
            else:
                reqObjects.headers['Connection'] = 'keep-alive'

        lastElement = False
        result = reqObjects.rawRequest() + CRLF + result
    result = result + CRLF
    #result = result + "GET /IDontExist HTTP/1.1" + CRLF + "Host: " + mainTarget + ":" + str(mainPort) +\
             #CRLF + "connection: close" + CRLF + CRLF
    return result

# TEST CODE #
def HTTPPipelineTest():
    result = False
    testReq1 = RequestObject('OPTIONS', 'https://0me.me/calc.php?a=2222&b=2','',
                             {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                              'Referer': 'https://www.google.com/',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                              'Accept-Language': 'en-GB,en;q=0.5',
                              'Max-Forwards': '0',
                              'Connection': 'close'})
    testReq2 = RequestObject('OPTIONS', 'https://0me.me/calc.php?a=3333&b=3','',
                             {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                              'Max-Forwards': '0','connection':'close'})
    testRequests = [testReq1,testReq2]
    pipelineResult = RequestObjectsToHTTPPipeline(testRequests)
    #print pipelineResult

    try:
        reqResult = SendHTTPRequestBySocket(pipelineResult, testReq1.targetName, testReq1.targetPort, testReq1.isSSL, 20)
    except:
        reqResult = ''
    #print reqResult
    if reqResult.find('4444') > 0 and reqResult.find('9999') > 0:
        result = True
    return result

def AnotherPipelineExample():
    req1 = RequestObject('GET', 'http://asitename.com:8080/sum.jsp?a=1&b=1&c=2&d=2')
    req2 = RequestObject('POST', 'http://asitename.com:8080/sum.jsp?a=3&b=3', 'c=4&d=4',
                         {'Content-Type': 'application/x-www-form-urlencoded'}, autoContentLength=True,
                         HTTPVersion="HTTP/1.0")
    req3 = RequestObject('POST', 'http://asitename.com:8080/sum.jsp?a=5&b=5', 'c=6&d=6',
                         {'Content-Type': 'application/x-www-form-urlencoded'}, autoContentLength=True)
    joinedReqs = [req1, req2, req3]
    pipelineResult = RequestObjectsToHTTPPipeline(joinedReqs)
    print SendHTTPRequestBySocket(pipelineResult, req1.targetName, req1.targetPort)


