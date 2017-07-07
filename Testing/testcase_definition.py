from string import Template
import os
import re

class TestcaseObject(object):
    _rawTemplate = ''
    templateRequest = Template('')
    selectRegExFromRequest = ''
    flagRegExStrInResponse = ''
    inverseFlag = False
    description = ''
    timeout = 0
    isEnabled = True
    isRateLimited = False
    sendInitialChars = 0
    sendBodyCharRate = 1
    delayInBetween = 0
    autoContentLength = False

    # The class "constructor" - It's actually an initializer
    def __init__(self, rawTemplate='',selectRegExFromRequest='',flagRegExStrInResponse='', inverseFlag=False,description='' ,isEnabled=True,timeout=0,
                 isRateLimited=False, sendInitialChars=0, sendBodyCharRate=1, delayInBetween=0, autoContentLength=False):

        self._rawTemplate = rawTemplate
        self.selectRegExFromRequest = selectRegExFromRequest
        self.flagRegExStrInResponse = flagRegExStrInResponse
        self.inverseFlag = inverseFlag
        self.description = description
        self.isEnabled = isEnabled
        self.timeout = timeout
        self.isRateLimited = isRateLimited
        self.sendInitialChars = sendInitialChars
        self.sendBodyCharRate = sendBodyCharRate
        self.delayInBetween = delayInBetween
        self.autoContentLength = autoContentLength
        self._setParams()

    def _setParams(self):
        self.templateRequest = Template(self._rawTemplate)

    def ReqBuilder(self, target_BoxObject):
        filename, extension = os.path.splitext(target_BoxObject.path)
        extension = extension[1:] # removing the dot character before the extension
        result = self.templateRequest.safe_substitute(ip=target_BoxObject.ip,
                                                    port=target_BoxObject.port,
                                                    path=target_BoxObject.path,
                                                    filename=filename,
                                                    extension=extension,
                                                    hostname=target_BoxObject.hostname,
                                                    description=target_BoxObject.description)

        if self.autoContentLength:
            bodylength = len(result) - re.search("(\r\n\r\n)|(\n\n)", result).end()
            if re.search("content\\-length", result, re.IGNORECASE):
                result = re.sub(r"(?i)content\-length:\s*\d+", "Content-Length: " + str(bodylength),
                                result, 1)
            else:
                result = re.sub(r"(\r\n\r\n)|(\n\n)", "\r\nContent-Length: " + str(bodylength) + "\r\n\r\n",
                                result, 1)

        return result
