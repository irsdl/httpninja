from django.http import HttpResponse
import re
import os

def index(request):
	result = "Test Page (at least vulnerable to xss - don't use on live)<br/>\n"
	try:
		result += "<br/>GET input0:<br/><br/>"
		result += "input0="+request.GET['input0']+"<br/>"
		result += "len(input0)="+str(len(request.GET['input0']))+"<br/>"
		result += "s.encode('utf-8')(input0)="+str(utf8len(request.GET['input0']))+"<br/><br/>"
	except:
		pass

	try:    
		result += "<br/>POST input1:<br/><br/>"
		result += "input1="+request.POST['input1']+"<br/>"
		result += "len(input1)="+str(len(request.POST['input1']))+"<br/>"
		result += "s.encode('utf-8')(input1)="+str(utf8len(request.POST['input1']))+"<br/><br/>"
	except:
		pass

	try:    
		result += "<br/>COOKIE input2:<br/><br/>"
		result += "input2="+request.COOKIES.get('input2')+"<br/>"
		result += "len(input2)="+str(len(request.COOKIES.get('input2')))+"<br/>"
		result += "s.encode('utf-8')(input2)="+str(utf8len(request.COOKIES.get('input2')))+"<br/><br/>"
	except:
		pass

		
	result += "<br/>\nGET:\n<br/>"
	for key, values in request.GET.lists():
		result += key + "=" + ', '.join(values) + "<br/>\n<br/>"     
	result += "\n<br/>POST:\n<br/>"
	for key, values in request.POST.lists():
		result += key + "=" + ', '.join(values) + "<br/>\n<br/>" 
	result += "\n<br/>HEADERS:\n<br/>"
	#regex_headers = re.compile(r'^(HTTP_.+|CONTENT_TYPE|CONTENT_LENGTH)$')
	#request_headers = {}
	for header in request.META:
		#if regex_headers.match(header):
			result +=   "{header}:{value}<br/>\n<br/>".format(header=header,value=request.META[header])
	
	for key in os.environ.keys():
		result = result + "%30s: %s <br/>\n" % (key,os.environ[key])

	return HttpResponse(result)


def utf8len(s):
  return len(s.encode('utf-8'))