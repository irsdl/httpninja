class BoxObject(object):
    ip = ''
    port = ''
    path = ''
    hostname = ''
    isSSL = False
    description = ''
    isEnabled = True
    # The class "constructor" - It's actually an initializer
    def __init__(self, ip='127.0.0.1',port='',path='',hostname='',isSSL=False,description='',isEnabled=True):
        self.ip = ip
        self.port = port
        self.path = path
        self.hostname = hostname
        self.isSSL = isSSL
        self.description = description
        self.isEnabled = isEnabled
        self._setParams()

    def _setParams(self):
        if self.hostname == '':
            self.hostname = self.ip

        if self.port == '':
            if self.isSSL:
                self.port = '443'
            else:
                self.port = '80'

        if self.path == '':
            self.path = '/'
