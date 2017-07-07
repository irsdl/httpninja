import config
import web_request_socket
from datetime import datetime
import codecs
import re
import testcase_mutation
import HTTPRequestHolder
import uuid

def logThis(message,type='log'):
    if type=='log':
        message = u"{delim}{time}{delim} {message}".format(delim="~"*30, time=datetime.now(),message=unicode(message, errors='ignore'))
        log_file = config.log_file
        print message
    else:
        log_file = config.result_file

    with codecs.open(log_file, "a","utf-8") as myfile:
        myfile.write(message+'\n')


def runTestcaseOnTarget(req_template,target_BoxObject):
    HTTPRequestHolderObjs = []
    initHTTPRequest = req_template.ReqBuilder(target_BoxObject)

    HTTPRequestHolderObjs.append(HTTPRequestHolder.HTTPRequestHolder(initHTTPRequest))

    if '$asciiChar' in initHTTPRequest or '${asciiChar}' in initHTTPRequest:
        HTTPRequestHolderObjs = testcase_mutation.asciiChar(HTTPRequestHolderObjs)

    if '$asciiHex' in initHTTPRequest or '${asciiHex}' in initHTTPRequest:
        HTTPRequestHolderObjs = testcase_mutation.asciiHex(HTTPRequestHolderObjs)

    if '$charset' in initHTTPRequest or '${charset}' in initHTTPRequest:
        HTTPRequestHolderObjs = testcase_mutation.encodingList(HTTPRequestHolderObjs)

    for HTTPRequestHolderObj in HTTPRequestHolderObjs:
        testUUID = str(uuid.uuid4())
        rawHTTPRequest = HTTPRequestHolderObj.rawHTTPRequest
        additionalInfo = HTTPRequestHolderObj.additionalInfo
        logThis("\n==Request to {ip} ({msgDesc}) - Template: {tempDesc} - TestID: {testID} - Additional Info:[{info}]==\n{message}".format(ip=target_BoxObject.ip,
                                                                                             msgDesc=target_BoxObject.description,
                                                                                             tempDesc=req_template.description,
                                                                                             testID=testUUID,
                                                                                             info=additionalInfo,
                                                                                             message=rawHTTPRequest),'log')
        timeout = config.timeout
        if req_template.timeout > 0:
            timeout = req_template.timeout

        result = web_request_socket.SendHTTPRequestBySocket(rawHTTPRequest=rawHTTPRequest,
                                                            targetName=target_BoxObject.ip,
                                                            targetPort=int(target_BoxObject.port),
                                                            isSSL=target_BoxObject.isSSL,
                                                            timeout=timeout,
                                                            includeTimeoutErr=False,
                                                            isRateLimited=req_template.isRateLimited,
                                                            sendInitialChars=req_template.sendInitialChars,
                                                            sendBodyCharRate=req_template.sendBodyCharRate,
                                                            delayInBetween=req_template.delayInBetween)

        statusCode = 'Unknown (HTTP v0.9?)'
        try:
            statusCode = re.search('HTTP/\d\.\d\s(\d+)', result).group(1)
        except:
            pass


        flagInResponseStringResult = ''
        if req_template.flagRegExStrInResponse != '':
            searchForRegexInResponse = req_template.flagRegExStrInResponse
            if req_template.selectRegExFromRequest != '' and '{selected_response}' in searchForRegexInResponse:
                requestPatternMatch = re.search(req_template.selectRegExFromRequest,rawHTTPRequest,re.MULTILINE)
                if requestPatternMatch is not None:
                    selected_response = re.escape(requestPatternMatch.group(0))
                    print selected_response
                    searchForRegexInResponse = searchForRegexInResponse.format(selected_response=selected_response)

            flagInResponseStringResult = ' - Flag ({flag}) result: '.format(flag=searchForRegexInResponse)
            searchForPattern = re.compile(searchForRegexInResponse)
            if (searchForPattern.search(result,re.MULTILINE) and not req_template.inverseFlag) or (not searchForPattern.search(result,re.MULTILINE) and req_template.inverseFlag):
                flagInResponseStringResult = flagInResponseStringResult + 'Flagged!'
                logThis("Success: [{tempDesc}] from [{ip}] ([{msgDesc}]) - Status code: [{statusCode}] - TestID: {testID} - Additional Info:[{info}]\n\n".format(
                    ip=target_BoxObject.ip,
                    msgDesc=target_BoxObject.description,
                    tempDesc=req_template.description,
                    statusCode=statusCode,
                    testID=testUUID,
                    info=additionalInfo), 'result')
            else:
                flagInResponseStringResult = flagInResponseStringResult + 'NotFlagged!'

        logThis("\n==Response from {ip} ({msgDesc}) - Template: {tempDesc}{flagInResponse} - TestID: {testID} - Additional Info:[{info}]==\n{message}".format(
            ip=target_BoxObject.ip,
            msgDesc=target_BoxObject.description,
            tempDesc=req_template.description,
            flagInResponse=flagInResponseStringResult,
            testID=testUUID,
            info=additionalInfo,
            message=result),'log')


if __name__=='__main__':
    for req_template in config.templates:
        if req_template.isEnabled:
            if config.sniper_mode is False:
                for target_BoxObject in config.target_boxes:
                    if target_BoxObject.isEnabled:
                        runTestcaseOnTarget(req_template, target_BoxObject)
            else:
                runTestcaseOnTarget(req_template, config.sniper_box)
