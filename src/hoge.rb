#!/usr/bin/env ruby
=begin
    This file is part of ks-generator.

    ks-generator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ks-generator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ks-generator.  If not, see <http://www.gnu.org/licenses/>.
=end
require "cgi-lib"
input = CGI.new
#print "Content-Type: text/html\n\n"

config ="#version RHEL6
text
install
url --url http://192.168.62.254/sl6
"


puts config
