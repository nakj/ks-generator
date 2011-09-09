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
#    input.each{|x|
#      p x
#    }
   p input
    print "<pre>"

    print "<br><br><br><br><br>"
    c = self.parse(input)    #general setting.
    c += self.parse2(input)  #disk partitioning.
    c += self.parse3(input)  #package section.
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
    post += net_post(input)
    post += hostname_post(input)
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
    ret =  "echo '"  + ret + "'>/etc/sysconfig/system-config-firewall\n"

    return ret
  end
  def net1(h,i)
    ret = ""
    
    #interface enable?
    if h['enable'] == "no" then
      return ""
    end
    file = sprintf("/etc/sysconfig/network-scripts/ifcfg-eth%d",i)

    # hardware address 
    unless h['mac'].length == 12 then
    ret+= "IF=eth" + i.to_s + "\n"
    end
    ret += "echo \""
    ret += "DEVICE=eth" + i.to_s + "\n"
    if h['mac'].length == 12 then
      mac = h['mac'].upcase
      ret += sprintf("HWADDR=%s:%s:%s:%s:%s:%s\n",mac[0..1],mac[2..3],mac[4..5],mac[6..7],mac[8..9],mac[10..11])
    else
      ret += "HWADDR=$(get_hwaddr ${IF})\n"
    end
    # boot protocol 
    if h['ipv4']['dhcp'] == "enable" then
      ret += sprintf("BOOTPROTO=dhcp\n")
    else
      ret += sprintf("BOOTPROTO=none\n")
      ret += sprintf("IPADDR=%s\n",h['ipv4']['ipaddr'])
      ret += sprintf("NETMASK=%s\n",h['ipv4']['netmask'])
    end
    ret += sprintf("\">%s\n",file)
    return ret
  end
  def net_post(input)
    ret = ""
    ret +='get_hwaddr ()
{
    if [ -f /sys/class/net/${1}/address ]; then
        awk \'{ print toupper($0) }\' < /sys/class/net/${IF}/address
    elif [ -d \"/sys/class/net/${1}\" ]; then
        LC_ALL= LANG= ip -o link show ${1} 2>/dev/null | \
           awk \'{ print toupper(gensub(/.*link\/[^ ]* ([[:alnum:]:]*).*/,
                                        \"\\1\", 1)); }\'
    fi
}
'
    h = {}
    r = []
    input.each{|x|
      n = []
      if x[0].match(/^net/) then
        n = x[0].split(/\s*\.\s*/)
        n << x[1]
        r << n
      end
    }

    b = []
    r.each{|x|
      b <<  x[1]
    }
     len = b.uniq.size
    i = 0
    while i < len
      h = {}
      ipv4={}
      a = []
      r.each{|x|
        if x[1] == i.to_s then
          a << x[2..4]
        end
      }
      a.each{|x|
        if x[0] == "ipv4" then
          ipv4[x[1]] = x[2]
        else
          h[x[0]] = x[1]
        end
        h['ipv4'] = ipv4
      }
      ret += self.net1(h,i)
      i += 1
    end
    # resolv.conf
    ret += 'echo "search '
    
    r.each{|x|
      if x[3] == "domain0" or x[3] == "domain1" then
        if x[4].length > 0 then
          ret +=  sprintf("%s ",x[4])
        end
      end
    }
    ret += "\n"
    r.each{|x|

      if x[3] == "dns" and x[4].length > 0 then
        ret += sprintf("nameserver %s\n", x[4])
      end
    }
    ret+= '">/etc/resolv.conf' + "\n"

    return ret
  end
  def hostname_post(input)
    ret=""
    r = []
    @networking = nil
    @hostname = ""

    input.each{|x|
      y = x[0].split(/\s*\.\s*/)
      y << x[1]
      if y[0] == "net" and y[2] == "enable" then
        r << y[3]
      end
      
    }
    if r.index("yes") >= 0 then
      @networking = "yes"
    else
      @networking = "no"
    end
    len = input['hostname'].length 
    if len  > 0 and len < 255 then
      @hostname = input['hostname']
    else
      @hostname = "localhost.localdomain"
    end
    ret += sprintf('echo "')
    ret += sprintf("NETWORKING=%s\n", @networking)
    ret += sprintf("HOSTNAME=%s\n", @hostname)
    ret += sprintf("\">/etc/sysconfig/network\n")
    return ret
  end


end  

if $0 == __FILE__ then
f = Foo.new
f.main
end
