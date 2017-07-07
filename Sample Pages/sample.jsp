<%@page pageEncoding="utf-8"%>
<%@page import="java.util.*"%>
Test Page (at least vulnerable to xss - don't use on live)<br/>
<%
out.println("<br/>Parameters:<br/><br/>");
Enumeration parameterList = request.getParameterNames();
while( parameterList.hasMoreElements())
{
	String sName = parameterList.nextElement().toString();
	String[] sMultiple = request.getParameterValues( sName );
	if( 1 >= sMultiple.length ){
		// parameter has a single value. print it.
		out.println("<br/>" + sName + "=" + request.getParameter( sName ) + "<br/>");
		out.println("-> Value Length: " + request.getParameter( sName ).length() +"<br/>" );
    out.println("-> Byte Value Length: " + request.getParameter( sName ).getBytes("UTF-8").length +"<br/>" );
	}else{
		for( int i=0; i<sMultiple.length; i++ ){
		  // if a paramater contains multiple values, print all of them
		  out.println("<br/>" + sName + "[" + i + "]=" + sMultiple[i] + "<br/>" );
		  out.println("-> Value Length: " + sMultiple[i].length() +"<br/>" );
      out.println("-> Byte Value Length: " + sMultiple[i].getBytes("UTF-8").length +"<br/>" );
    }
  }
}

out.println("<br/>COOKIE input2:<br/><br/>");
Cookie cookie = null;
Cookie[] cookies = null;
cookies = request.getCookies();
if( cookies != null)
 {
        for (int i = 0; i < cookies.length; i++){
                cookie = cookies[i];
                if (cookie.getName().equals("input2"))
                        out.println("<br/>input2="+cookie.getValue()+"<br/>");
        }
}
out.println("<br/>");

out.println("<br/>Headers:<br/><br/>");
java.util.Enumeration names=request.getHeaderNames();
while (names.hasMoreElements()) {
	String name = (String) names.nextElement();
	String value = request.getHeader(name);
	out.println("<br/>"+name + "=" + value+"<br/>");
}

out.println("<br/>");
out.println("<br/>Servlet Equivalent of Standard CGI Variables:<br/><br/>");
%>
<pre>
AUTH_TYPE:       <%= request.getAuthType() %>
CONTENT_LENGTH:  <%= request.getContentLength() %>
CONTENT_TYPE:    <%= request.getContentType() %>
PATH_INFO:       <%= request.getPathInfo() %>
PATH_TRANSLATED: <%= request.getPathTranslated() %>
QUERY_STRING:    <%= request.getQueryString() %>
REMOTE_ADDR:     <%= request.getRemoteAddr() %>
REMOTE_HOST:     <%= request.getRemoteHost() %>
REMOTE_USER:     <%= request.getRemoteUser() %>
REQUEST_METHOD:  <%= request.getMethod() %>
SCRIPT_NAME:     <%= request.getServletPath() %>
SERVER_NAME:     <%= request.getServerName() %>
SERVER_PORT:     <%= request.getServerPort() %>
SERVER_PROTOCOL: <%= request.getProtocol() %>
SERVER_SOFTWARE: <%= getServletContext().getServerInfo() %>
Request URI:          <%= request.getRequestURI() %>
Request URL:          <%= request.getRequestURL() %>
Request Context Path: <%= request.getContextPath() %>
Real Path:            <%= getServletContext().getRealPath("/") %>
</pre>