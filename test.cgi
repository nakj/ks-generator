#!/usr/bin/ruby
require "cgi-lib"
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
class Foo
  def main
    input = CGI.new
    print "Content-Type: text/html\n\n"
    print "<html><body>inputdata= "

    p input

    print "<br><br><br><br><br>"
    c = self.parse(input)
    self.output(c)
    print "</body></html>"
  end
  def parse(input)
    config ="#version RHEL6
text
install
url --url http://192.168.62.254/sl6
"
    if input['lang'] == "other" then
      lang = input['lang_other']
    else
      lang = input['lang']
    end
    config += "lang #{lang}\n" 
    #keyboard
    if input['kbd'] == "other" then
      kbd = "keyboard " + input['kbd_other'] + "\n"
    else
      kbd = "keyboard jp106" + "\n"
    end
    config += kbd
    if input['grub'] == "true" then
      grub = "bootloader --location=mbr --append=\"rhgb quiet\""
      if input['grubpw'] == "true" then
        grub = sprintf("%s --password %s",grub,input['grubpasswd'])
      end
      grub += "\n"
    end 
    config += grub

    if input['rootpw'] == "other" then
      rootpw = "rootpw #{input['rootpass']}\n"
    else
      rootpw = "rootpw #{input['rootpw']}\n"
    end
    config += rootpw
    return config
  end


  def output(config)
    print "<pre>"
    puts config
    print "</pre>"
  end
end  


f = Foo.new
f.main
