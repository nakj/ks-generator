#!/usr/bin/env ruby
# -*- coding: utf-8 -*-
require "cgi-lib"
require "config/config"
require "config/rhel6"

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
    print "<pre>"
    input.each{|x|
      p x
    }
#   p input
    print "<pre>"

    print "<br><br><br><br><br>"
    c = self.parse(input)    #general setting.
    c += self.parse2(input)  #disk partitioning.
    c += self.parse3(input)  #package selection.
    c += self.parse4(input)  #%post section
    self.output(c)
    print "</body></html>"
  end
  def parse(input)
    config ="#version RHEL6
text
install

url --url #{$url}

firstboot --disable
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

    #timezone
    if input['tz'] then
      tz = "timezone #{input['tz']} "
    end
    if input['utc'] then
      tz += "--utc\n"
    end
    tz += "\n"
    config += tz
    
    #firewall 
    fw  = ""
    if input['firewall'] == "enabled" then
      fw = "firewall --enabled"
      services = ["ssh","telnet","smtp","http","ftp"]
      services.each{|s|
        if input["fw."+s] then
          fw += " --" + s 
        end
	}	
      $srvs.each{|x|
      if input["fw." + x['srv']] then
        #p x['srv']
        unless x['ports'] == nil then
          x['ports'].each{|y|
            fw += sprintf(" --port=%d:%s",y[0],y[1])
          }
        end
      end

    }

    elsif input['firewall'] == "disabled" then
      fw = "firewall --disabled"
    end
    fw += "\n"
    config += fw

    #selinux
    sl = ""
    if input['selinux']  then
      sl += "selinux --" + input['selinux']
      sl += "\n"

    end
    config += sl

    return config
  end


  def parse2(input)
    #disk layout
    config =""

    config += self.part(0,input)


    return config
  end
  def parse3(input)
    # packages
    pl = $pkglist
    config = ""
    config += "#Package Selection\n"
    config += "%packages\n"

    pkgs = ""
    pl.each{|g|
      gr = "pkg." + g 
      if input[gr] then
        pkgs += "@#{g}\n"
      end 
    }
    config += pkgs
    return config
  end
  def parse4(input)
    post = "#Script section\n"
    post += "%post\n"
    post += fw_post(input)
    return post
  end

  def output(config)
    print "<pre>"
    puts config
    print "</pre>"
    f = File.open("tmp/ks.cfg","w")
    f.puts(config)
  end
  def part(i,input)
    if input["disk#{i}.modify"] == "nomodify" then
      return ""
    end
    #input からディスクi に関するところだけ抜き出す
    re = "^disk"  + i.to_s
    di = {}
    di['fstype'] = input['fstype']

    input.each_pair{|key,value|
      if key.match(re) then
        unless value == "" then
          #puts "#{key}: #{value}"
          key = key.gsub(/^disk#{i}./,"")
          di[key] = value
        end
      end
    
    }
=begin
#debug よう
  di.sort.each{|x|
    p x
  }
=end  
    ret = ""
    s = ""
    if di["modify"] == "clearpart"  then
      ret += "clearpart --all --drives=#{di['name']}\n"
    end
    for i in 1..10
      s = slices(i,di)
      unless s == nil then
        ret += s
      end

    end
    return ret

  end

  def slices(i,di)
    dsk = di['name']

    label = di["part#{i}.label"]
    odd = di['odd'].gsub(/^disk[0-9]\.part/,"").gsub(/.odd$/,"")
    parttype = di["part#{i}.parttype"]
    fs = di['fstype']
    if label == "swap" then
      fs = "swap"
    end
    if odd.to_i == i then
      size = "grow"
    else
      size = di["part#{i}.size"]
    end
    unless size == nil then
      if size == "grow" then
        ret = "part #{label} --fstype=#{fs} --size=1 --grow --ondisk=#{dsk}"
      else 
        ret = "part #{label} --fstype=#{fs} --size=#{size} --ondisk=#{dsk}"
      end
      if parttype == "primary" then
        ret += " --asprimary"
      end
      ret += "\n"
      return ret
    end
  end
  def fw_post(input)
    ret = "# Configuration file for system-config-firewall\n\n"
    if input['firewall'] == "enabled" then
      ret += "--enabled\n"
    elsif input['firewall'] == "disabled" then
      ret += "--disabled\n"
    end
    services = ["ssh","telnet","smtp","http","ftp"]
    services.each{|x|
      if input["fw." + x] then
        ret += "--service=" + x + "\n"
      end
      }	
    $srvs.each{|x|
      if input["fw." + x['srv']] then
        ret += "--service=" + x['srv'] + "\n"
      end
    }
    ret =  "echo '"  + ret + "'>/etc/sysconfig/system-config-firewall"

    return ret
  end


end  

if $0 == __FILE__ then
f = Foo.new
f.main
end
