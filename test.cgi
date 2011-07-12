#!/usr/bin/ruby
require "cgi-lib"

input = CGI.new
print "Content-Type: text/html\n\n"



print "<html><body>inputdata= "

p input



print "</body></html>"
