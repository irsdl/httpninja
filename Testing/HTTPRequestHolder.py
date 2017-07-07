class HTTPRequestHolder(object):
    rawHTTPRequest = ''
    additionalInfo = ''

    # The class "constructor" - It's actually an initializer
    def __init__(self, rawHTTPRequest='', additionalInfo=''):
        self.rawHTTPRequest = rawHTTPRequest
        self.additionalInfo = additionalInfo

