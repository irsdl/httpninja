import box_definition
import testcase_definition

log_file = 'logs.txt'
result_file = 'results.txt'

timeout = 3
sniper_mode = False # This will only use the sniper_box settings

target_boxes = []
# we can have multiple targets
target_boxes.append(box_definition.BoxObject(ip='192.168.1.1',port='80',path='/sample.mypy',hostname='test.com',isSSL=False,description='Nginx-django-py3',isEnabled=False))
target_boxes.append(box_definition.BoxObject(ip='192.168.1.2',port='80',path='/sample.php',hostname='victim.com',isSSL=False,description='Apache-php5-mod_php behind WAF'))
target_boxes.append(box_definition.BoxObject(ip='192.168.1.3',port='80',path='/sample.jsp',hostname='',isSSL=False,description='Apache Tomcat7 Java 1.6 behind squid',isEnabled=True))
target_boxes.append(box_definition.BoxObject(ip='192.168.1.4',port='80',path='/sample.asp',hostname='',isSSL=False,description='IIS10-ASP Classic'))
target_boxes.append(box_definition.BoxObject(ip='192.168.1.5',port='80',path='/sample.aspx',hostname='',isSSL=False,description='IIS10-ASPX (v4.x)'))

# we can only have one sniper box
sniper_box = box_definition.BoxObject(ip='127.0.0.1',port='443',path='/specifictarget',hostname='mytest.com',isSSL=True,description='something')

templates = []
# we can have multiple templates
templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET $path?input0=test0 HTTP/1.1
HOST: $ip
Connection: Close

""", description='Normal GET', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='Normal POST', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST as GET', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""XXX $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='XXX as POST', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""[]'{}$&*() $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='[]\'{}$&*() as POST', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.1)-Multiple Content-Length - Wrong First', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Content-Length: 0
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.1)-Multiple Content-Length - Wrong Second', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.1)-No Content-Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content_Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.1)-Content_Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.1)-Smaller Content-Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 100
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.1)-Larger Content-Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.0)-Multiple Content-Length - Wrong First', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Content-Length: 0
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.0)-Multiple Content-Length - Wrong Second', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.0)-No Content-Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content_Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.0)-Content_Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.0)-Smaller Content-Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 100
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST (HTTP/1.0)-Larger Content-Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET $path?input0=test31337 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test31337', description='GET (HTTP/1.0)-Multiple Content-Length - Wrong First', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET $path?input0=test31337 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Content-Length: 0
Connection: Close

input1=test1337""", flagRegExStrInResponse='test31337', description='GET (HTTP/1.0)-Multiple Content-Length - Wrong Second', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET $path?input0=test31337 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Connection: Close

input1=test1337""", flagRegExStrInResponse='test31337', description='GET (HTTP/1.0)-Smaller Content-Length', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET $path?input0=test31337 HTTP/1.0
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 100
Connection: Close

input1=test1337""", flagRegExStrInResponse='test31337', description='GET (HTTP/1.0)-Larger Content-Length', isEnabled=False))



templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $ip
Content-Type: application/x-www-form-urlencoded
Content-Length: 25
Connection: Close

input1=test1337AAAAAAAAAA""", flagRegExStrInResponse='test1337', description='Content-Length with Slow Completion by Socket',
                    timeout=100, isRateLimited=True, sendInitialChars=145, sendBodyCharRate=1, delayInBetween=0.2, isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='Multiple HOST (both the same)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
HOST: foobar.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='Multiple HOST (first one valid)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: foobar.com
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='Multiple HOST (second one valid)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://foobar.com$path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='Different invalid HOST Name in Path valid in header', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://$hostname$path?input0=test0 HTTP/1.1
HOST: foobar.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='Different valid HOST Name in Path invalid in header', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: []'{}$&*() as HOST
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='[]\'{}$&*() as HOST', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: {}'$&(^_-.`)#!~
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='{}\'$&(^_-.`)#!~ as HOST', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: foobar.com@$hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='invalid@valid as HOST', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://foobar.com@$hostname$path?input0=test0 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='invalid@valid as HOST in PATH with no HOST - HTTP1.1', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://foobar.com@$hostname$path?input0=test0 HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='invalid@valid as HOST in PATH with no HOST - HTTP1.0', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: 
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='Empty HOST', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://invalid@$path?input0=test0 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='invalid@empty as HOST in PATH with no HOST  - HTTP1.1', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://invalid@$path?input0=test0 HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='invalid@empty as HOST in PATH with no HOST  - HTTP1.0', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http$asciiChar://$hostname$path?input0=test0 HTTP/1.1
Host: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='http+asciiChar as protocol', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
Host: $hostname:45678
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='45678', description='HOST Port Manipulation in header', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://$hostname:45678$path?input0=test0 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='45678', description='HOST Port Manipulation in path with no HOST header on HTTP/1.1', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://$hostname:45678$path?input0=test0 HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='45678', description='HOST Port Manipulation in path with no HOST header on HTTP/1.0', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://$hostname:45670$path?input0=test0 HTTP/1.1
Host: $hostname:45679
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='4567', description='HOST Port Manipulation in header and path', isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET $path?input0=test1337
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1234""", flagRegExStrInResponse='test1337', description='GET with HTTP v0.9 with relative path', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1234""", flagRegExStrInResponse='test1337', description='GET with HTTP v0.9 with absolute path', isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST with HTTP v0.9 with relative path', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://$hostname$path?input0=test0
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Connection: Close

input1=test1337""", flagRegExStrInResponse='test1337', description='POST with HTTP v0.9 with absolute path', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/0.123
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/0.123)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/1.10000000
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with GET with invalid HTTP version (HTTP/1.10000000)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/00000001.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/00000001.1)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/1.10
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/1.10)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/1.19
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/1.19)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/2.0
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/2.0)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/.9
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/.9)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/0.99
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/0.99)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP/9.9
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/9.9)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 HTTP${asciiChar}1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (HTTP/9.9)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 XXXX/0.123
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (XXXX/1.1)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""GET http://$hostname$path?input0=test1337000 XXXX
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337000', description='GET with invalid HTTP version (XXXX)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://$hostname$path?input0=test1337000 HTTP/0.9
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337111', description='POST with invalid HTTP version (HTTP/0.9)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://$hostname$path?input0=test1337000 XXXX
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337111', description='POST with invalid HTTP version (XXXX)', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test1337000 HTTP/1.1
HOST: $hostname$asciiChar
Content-Type: application/x-www-form-urlencoded
Content-Length: 37
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337111', description='valid  characters in host header', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test1337000 HTTP/1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
Connection: Close

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337222', description='Additional character after final character (based on length) - connection: close', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test1337000 HTTP/1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 36
Connection: keep-alive

input1=test1337111&input0=test1337222""", flagRegExStrInResponse='test1337222', description='Additional character after final character (based on length) - connection: keep-alive', isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Cont${asciiChar}ent-Length: 15
Connection: close

input1=test1337""", flagRegExStrInResponse='test1337', description='Ignored characters in the middle of valid header names such as content-length', isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length: 1${asciiChar}5
Connection: close

input1=test1337""", flagRegExStrInResponse='test1337', description='Ignored characters in the middle of valid header names such as content-length', timeout=1, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
${asciiChar}Content-Length: 15
Connection: close

input1=test1337""", flagRegExStrInResponse='test1337', description='Valid characters before headers', timeout=1, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: application/x-www-form-urlencoded
Content-Length${asciiChar}: 15
Connection: close

input1=test1337""", flagRegExStrInResponse='test1337', description='Valid characters after headers before colon', timeout=1, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname${asciiChar}Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='test1337', description='Valid header separators', timeout=1, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15${asciiChar}
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='test1337', description='Valid characters after content-length values', timeout=1, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 17
Content-Type: application/x-www-form-urlencoded${asciiChar}
Connection: close

input1=test133%37""", flagRegExStrInResponse='input1=test1337', description='Valid characters after content-type values', timeout=1, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length:${asciiChar} 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Valid characters before headers values after colon before space in content-length', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type:${asciiChar} application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Valid characters before headers values after colon before space in content-type', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
TEST
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Empty header without colon', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: ${asciiChar}application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Valid characters before headers values after colon before space in content-type (POST)', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: appli${asciiChar}cation/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Valid characters in the middle of "application" in in "Content-Type: application/x-www-form-urlencoded"', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-fo${asciiChar}rm-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Valid characters in the middle of "form" in in "Content-Type: application/x-www-form-urlencoded"', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $filename${asciiChar}.$extension?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Ignored characters after file path before extension', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path${asciiChar}?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Ignored characters after file path', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST /${asciiChar}$filename.$extension?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Ignored characters before file path', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST %2F$path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Start path with %2F rather than /', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST /%2F/$path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Start path with /%2F/', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST /%2E/$path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='Start path with /%2E/', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST /$filename%u002e$extension?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input1=test1337', description='. character replacement before extension with %u002e', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: multipart/form-data; boundary=--------deilim123
Connection: close
Content-Length: 0

----------deilim123\r\nContent-Disposition: form-data; name="input1"\r\n\r\ntest1337\r\n----------deilim123--""",
flagRegExStrInResponse='input1=test1337', description='Converting "application/x-www-form-urlencoded" to "multipart/form-data" in normal POST (CR LF between multiparts)', timeout=10, autoContentLength=True, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: multipart/form-data; boundary=--------deilim123
Connection: close
Content-Length: 0

----------deilim123\r\nContent-Disposition: form-data; name="input1"\r\n\r\ntest1337""",
flagRegExStrInResponse='>input1=test1337', description='Converting "application/x-www-form-urlencoded" to "multipart/form-data" in normal POST (CR LF between multiparts) - Missing last boundary', timeout=10, autoContentLength=True, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: multipart/form-data; boundary=--------deilim123
Connection: close
Content-Length: 0

----------deilim123\nContent-Disposition: form-data; name="input1"\n\ntest1337\n----------deilim123--""",
flagRegExStrInResponse='input1=test1337', description='Converting "application/x-www-form-urlencoded" to "multipart/form-data" in normal POST (LF between multiparts)', timeout=10, autoContentLength=True, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: multipart/form-data; boundary=--------deilim123
Connection: close
Content-Length: 0

----------deilim123\r\nContent-Disposition: name="input1"\r\n\r\ntest1337\r\n----------deilim123--""",
flagRegExStrInResponse='>input1=test1337', description='"multipart/form-data" in normal POST (CR LF between multiparts) - Missing form-data in Content-Disposition', timeout=10, autoContentLength=True, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: multipart/form-data; boundary=--------deilim123
Connection: close
Content-Length: 0

----------deilim123Content-Disposition: form-data; name="input1"\r\n\r\ntest1337\r\n----------deilim123--""",
flagRegExStrInResponse='>input1=test1337', description='"multipart/form-data" in normal POST (CR LF between multiparts) - No character between Content-Disposition and the boundary', timeout=10, autoContentLength=True, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Type: multipart/form-data; boundary=--------deilim123
Connection: close
Content-Length: 0

----------deilim123\r\nContent-Disposition: name="input1"; form-data;\r\n\r\ntest1337\r\n----------deilim123--""",
flagRegExStrInResponse='>input1=test1337', description='"multipart/form-data" in normal POST (CR LF between multiparts) - name before form-data in Content-Disposition', timeout=10, autoContentLength=True, isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=testGET HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
COOKIE: input0=testCOOKIE
input0: testHEADER
Connection: close

input0=testPOST""", flagRegExStrInResponse='input0=', description='One parameter in GET/POST/COOKIES/HEADER - reading GET', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input1=testGET HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
COOKIE: input1=testCOOKIE
input1: testHEADER
Connection: close

input1=testPOST""", flagRegExStrInResponse='input1=', description='One parameter in GET/POST/COOKIES/HEADER - reading POST', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test111&input0=test222&input0=test333 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input0=', description='Multiple GET Parameters with the same name', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 0
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test111&input1=test222&input1=test333""", flagRegExStrInResponse='input0=', description='Multiple POST Parameters with the same name', timeout=3, autoContentLength=True, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test0 HTTP/1.1
HOST: $hostname
Content-Length: 15
Cookie: input2=test111;input2=test222;input2=test333;
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1337""", flagRegExStrInResponse='input2=', description='Multiple Cookie Parameters with the same name', timeout=3, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0${asciiChar}=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='input0=test1337', description='Ignored characters after parameter name (GET) - before = sign', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0%${asciiHex}=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='input0=test1337', description='Ignored url-encoded characters after parameter name (GET) - before = sign', timeout=5, isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?${asciiChar}input0=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='[^>]>input0=test1337', description='Ignored characters before parameter name (GET) - before = sign', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?%${asciiHex}input0=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='[^>]>input0=test1337', description='Ignored url-encoded characters before parameter name (GET) - before = sign', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?inp${asciiChar}ut0=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='input0=test1337', description='Ignored characters in the middle of parameter name (GET) - before = sign', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?inp%${asciiHex}ut0=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='input0=test1337', description='Ignored url-encoded characters in the middle of parameter name (GET) - before = sign', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: foo=bar${asciiChar}input2=test1337;
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337', description='; character replacement in Cookie', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: input2${asciiChar}test1337;
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337', description='; character replacement in Cookie', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: inp${asciiChar}ut2=test1337;
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337', description='Ignored characters in Cookie name', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: input2=test${asciiChar}1337;
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337', description='Ignored characters in Cookie value', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?foo=bar${asciiChar}input0=test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337', description='& character replacement in GET', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?foo=bar%${asciiHex}input0=test HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337', description='& character replacement in GET (url-encoded)', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0${asciiChar}test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337', description='= character replacement in GET', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0%${asciiHex}test HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337', description='= character replacement in GET (url-encoded)', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test1337${asciiChar} HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337<[^<\s]', description='Ignored characters after parameter value (GET)', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test1337%${asciiHex} HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337<[^<\s]', description='Ignored url-encoded characters after parameter value (GET)', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=${asciiChar}test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337<[^<\s]', description='Ignored characters before parameter value (GET) - after = sign', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=%${asciiHex}test1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337<[^<\s]', description='Ignored url-encoded characters before parameter value (GET) - after = sign', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test${asciiChar}1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337<[^<\s]', description='Ignored characters in the middle of parameter value (GET)', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test%${asciiHex}1337 HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input0=test1337<[^<\s]', description='Ignored url-encoded characters in the middle of parameter value (GET)', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=1 HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: inpu%742=test1337
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337<[^<\s]', description='URL Encoding in Cookie parameter name', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=1 HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: input2=tes%741337
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337<[^<\s]', description='URL Encoding in Cookie parameter value', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=1 HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: inpu%u00742=test1337
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337<[^<\s]', description='utf-8 Encoding (%uHHHH) in Cookie parameter name', timeout=5, isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=1 HTTP/1.1
HOST: $hostname
Content-Length: 12
Cookie: input2=tes%u00741337
Content-Type: application/x-www-form-urlencoded
Connection: close

input1=test1""", flagRegExStrInResponse='>input2=test1337<[^<\s]', description='utf-8 Encoding (%uHHHH) in Cookie parameter value', timeout=5, isEnabled=False))


templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=1 HTTP/1.1
HOST: $hostname
Content-Length: 15
Content-Type: application/x-www-form-urlencoded; charset=${charset}
Connection: close

input1=test1337""", flagRegExStrInResponse='(^i|>i)nput1=test1337<[^<\s]', inverseFlag=True, description='utf-8 Encoding (%uHHHH) in Cookie parameter value', timeout=5, isEnabled=False))








# perhaps for sniper use

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST $path?input0=test HTTP/1.1
HOST: $hostname
Content-Length: 12
Content-Type: application/x-www-form-urlencoded
Cookie: input2${asciiChar}=test2
Connection: close

input1=test1""", selectRegExFromRequest='input2([^=]|=)', flagRegExStrInResponse='\[{selected_response}\]',
inverseFlag=True, description='Normal ASCII character conversion in GET (URL) paramater name', timeout=5, isEnabled=False))

templates.append(testcase_definition.TestcaseObject(rawTemplate=
"""POST http://0me.me/calc.php?a=2222&b=2 HTTP/1.0
Host: 0me.me
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

c=3333&d=3POST http://0me.me/calc.php?a=1111&b=1 HTTP/1.1
Host: 0me.me
Content-Type: application/x-www-form-urlencoded
Content-Length: 9

c=7&d=191""", flagRegExStrInResponse='test1337', description='Sniper Related - HTTP Pipelining, 1 character every 200 milisec',
                    timeout=100, isRateLimited=False, sendInitialChars=1, sendBodyCharRate=1, delayInBetween=0.2, isEnabled=False))