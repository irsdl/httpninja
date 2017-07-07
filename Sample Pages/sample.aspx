Test Page (at least vulnerable to xss - don't use on live)<br/>
<%
On Error Resume Next
Response.write("<br/>GET input0:<br/>")
Response.write("<br/>input0="&(Request.querystring("input0"))&"<br/>")
Response.write("Len(input0)="&Len(Request.querystring("input0"))&"<br/>")
Response.write("System.Text.Encoding.Unicode.GetByteCount(input0)="&System.Text.Encoding.Unicode.GetByteCount(Request.querystring("input0"))&"<br/><br/>")

Response.write("<br/>POST input1:<br/>")
Response.write("<br/>input1="&(Request.form("input1"))&"<br/>")
Response.write("Len(input1)="&Len(Request.form("input1"))&"<br/>")
Response.write("System.Text.Encoding.Unicode.GetByteCount(input1)="&System.Text.Encoding.Unicode.GetByteCount(Request.form("input1"))&"<br/><br/>")

Response.write("<br/>COOKIE input2:<br/>")
Response.write("<br/>input2="&(Request.Cookies("input2").Value)&"<br/>")
Response.write("Len(input2)="&Len(Request.Cookies("input2").Value)&"<br/>")
Response.write("System.Text.Encoding.Unicode.GetByteCount(input2)="&System.Text.Encoding.Unicode.GetByteCount(Request.Cookies("input2").Value)&"<br/><br/>")

Response.write("<br/>All GET:<br/><br/>")
For each item in request.querystring
	Response.write("<br/>" & item & "="&request.querystring(item)&"<br/>")
	Response.write("<br/>")
Next

Response.write("<br/>All POST:<br/>")
For each item in request.form
	Response.write("<br/>" & item & "="&request.form(item)&"<br/>")
Next

Response.write("<br/>All COOKIES:<br/><br/>")
For each item in request.Cookies
	Response.write("<br/>" & item & "="&request.Cookies(item)&"<br/>")
	Response.write("<br/>")
Next

Response.write("<br/>Server Variables:<br/><br/>")
For each item in Request.ServerVariables
	Response.write("<br/>" & item & "="&Request.ServerVariables(item)&"<br/>")
	Response.write("<br/>")
Next

Response.write("<br/>generic parameter ( REQUEST(""input"") ) input:<br/>")
Response.write("<br/>input="&(Request("input"))&"<br/>")
Response.write("Len(input)="&Len(Request("input"))&"<br/>")
Response.write("System.Text.Encoding.Unicode.GetByteCount(input)="&System.Text.Encoding.Unicode.GetByteCount(Request("input"))&"<br/><br/>")
%>