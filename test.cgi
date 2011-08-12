#!/usr/bin/ruby
# -*- coding: utf-8 -*-
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
    $pkglist = ["storage-client-fcoe", "infiniband", "java-platform", "perl-runtime", "storage-client-iscsi", "client-mgmt-tools", "console-internet", "storage-client-multipath", "smart-card", "security-tools", "dial-up", "directory-client", "debugging", "network-tools", "network-file-system-client", "hardware-monitoring", "backup-client", "performance", "base", "mainframe-access", "legacy-unix", "compat-libraries", "print-client", "large-systems", "scientific", "", "cifs-file-server", "ftp-server", "nfs-file-server", "server-platform", "system-admin-tools", "directory-server", "network-server", "storage-server", "backup-server", "print-server", "identity-server", "mail-server", "", "php", "turbogears", "web-server", "web-servlet", "", "mysql", "mysql-client", "postgresql", "postgresql-client", "", "system-management-snmp", "system-management-wbem", "system-management", "system-management-messaging-server", "system-management-messaging-client", "", "virtualization", "virtualization-client", "virtualization-tools", "virtualization-platform", "", "kde-desktop", "x11", "graphical-admin-tools", "basic-desktop", "desktop-debugging", "desktop-platform", "fonts", "remote-desktop-clients", "legacy-x", "input-methods", "general-desktop", "", "emacs", "tex", "internet-browser", "graphics", "technical-writing", "", "eclipse", "additional-devel", "server-platform-devel", "desktop-platform-devel", "development", "", "icelandic-support", "irish-support", "azerbaijani-support", "assamese-support", "afrikaans-support", "amazigh-support", "arabic-support", "albanian-support", "armenian-support", "italian-support", "inuktitut-support", "interlingua-support", "indonesian-support", "welsh-support", "ukrainian-support", "uzbek-support", "urdu-support", "estonian-support", "esperanto-support", "ethiopic-support", "dutch-support", "oriya-support", "kazakh-support", "kashmiri-support", "kashubian-support", "catalan-support", "kannada-support", "galician-support", "greek-support", "khmer-support", "kurdish-support", "croatian-support", "gujarati-support", "georgian-support", "gaelic-support", "xhosa-support", "coptic-support", "konkani-support", "sardinian-support", "sanskrit-support", "sindhi-support", "sinhala-support", "swedish-support", "spanish-support", "slovak-support", "slovenian-support", "swati-support", "swahili-support", "zulu-support", "serbian-support", "somali-support", "tsonga-support", "thai-support", "tagalog-support", "tajik-support", "tamil-support", "czech-support", "chichewa-support", "tibetan-support", "chhattisgarhi-support", "tswana-support", "tetum-support", "telugu-support", "danish-support", "turkmen-support", "turkish-support", "german-support", "southern-ndebele-support", "nepali-support", "norwegian-support", "hungarian-support", "basque-support", "punjabi-support", "hiligaynon-support", "hindi-support", "fijian-support", "filipino-support", "finnish-support", "faroese-support", "french-support", "friulian-support", "frisian-support", "brazilian-support", "bulgarian-support", "breton-support", "bhutanese-support", "hebrew-support", "vietnamese-support", "belarusian-support", "bengali-support", "venda-support", "persian-support", "portuguese-support", "polish-support", "maithili-support", "maori-support", "macedonian-support", "malagasy-support", "malayalam-support", "marathi-support", "maltese-support", "malay-support", "manx-support", "burmese-support", "mongolian-support", "lao-support", "latin-support", "latvian-support", "lithuanian-support", "luxembourgish-support", "kinyarwanda-support", "romanian-support", "occitan-support", "russian-support", "walloon-support", "chinese-support", "low-saxon-support", "northern-sotho-support", "southern-sotho-support", "japanese-support", "british-support", "korean-support", "upper-sorbian-support"]

$ports = ["amanda-client","bacula","bacula-client","dns","ftp","ipsec","nfs","openvpn","radius","cluster-suite","ssh","imaps","pop3s","samba","samba-client","tftp","tftp-client","http","ipp-client","ipp","mdns","smtp","libvirt","libvirt-tls","https"]
$srvs = [{"srv"=>"ipp-client", "ports"=>[["631", "udp"]]}, {"srv"=>"ipp", "ports"=>[["631", "tcp"], ["631", "udp"]]}, {"srv"=>"mdns", "ports"=>[["5353", "udp"]]}, {"srv"=>"ipsec", "ports"=>[["500", "udp"]]}, {"srv"=>"nfs", "ports"=>[["2049", "tcp"]]}, {"srv"=>"https", "ports"=>[["443", "tcp"]]}, {"srv"=>"samba-client", "ports"=>[["137", "udp"], ["138", "udp"]]}, {"srv"=>"samba", "ports"=>[["137", "udp"], ["138", "udp"], ["139", "tcp"], ["445", "tcp"]]}, {"srv"=>"dns", "ports"=>[["53", "tcp"], ["53", "udp"]]}, {"srv"=>"imaps", "ports"=>[["993", "tcp"]]}, {"srv"=>"pop3s", "ports"=>[["995", "tcp"]]}, {"srv"=>"radius", "ports"=>[["1812", "udp"], ["1813", "udp"]]}, {"srv"=>"openvpn", "ports"=>[["1194", "udp"]]}, {"srv"=>"tftp", "ports"=>[["69", "udp"]]}, {"srv"=>"tftp-client", "ports"=>nil}, {"srv"=>"cluster-suite", "ports"=>[["5404", "udp"], ["5405", "udp"], ["11111", "tcp"], ["21064", "tcp"]]}, {"srv"=>"amanda-client", "ports"=>[["10080", "udp"]]}, {"srv"=>"bacula-client", "ports"=>[["9102", "tcp"]]}, {"srv"=>"bacula", "ports"=>[["9101", "tcp"], ["9102", "tcp"], ["9103", "tcp"]]}, {"srv"=>"libvirt", "ports"=>[["16509", "tcp"]]}, {"srv"=>"libvirt-tls", "ports"=>[["16509", "tcp"]]}]



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
url --url http://192.168.56.254/rhel6

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

    $srvs.each{|x|
      if input["fw." + x['srv']] then
        ret += "--service=" + x['srv'] + "\n"
      end
    }
    ret =  "echo '"  + ret + "'>/etc/sysconfig/system-config-firewall"

    return ret
  end


end  


f = Foo.new
f.main
