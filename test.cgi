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
    $pkglist = ["storage-client-fcoe", "infiniband", "java-platform", "perl-runtime", "storage-client-iscsi", "client-mgmt-tools", "console-internet", "storage-client-multipath", "smart-card", "security-tools", "dial-up", "directory-client", "debugging", "network-tools", "network-file-system-client", "hardware-monitoring", "backup-client", "performance", "base", "mainframe-access", "legacy-unix", "compat-libraries", "print-client", "large-systems", "scientific", "", "cifs-file-server", "ftp-server", "nfs-file-server", "server-platform", "system-admin-tools", "directory-server", "network-server", "storage-server", "backup-server", "print-server", "identity-server", "mail-server", "", "php", "turbogears", "web-server", "web-servlet", "", "mysql", "mysql-client", "postgresql", "postgresql-client", "", "system-management-snmp", "system-management-wbem", "system-management", "system-management-messaging-server", "system-management-messaging-client", "", "virtualization", "virtualization-client", "virtualization-tools", "virtualization-platform", "", "kde-desktop", "x11", "graphical-admin-tools", "basic-desktop", "desktop-debugging", "desktop-platform", "fonts", "remote-desktop-clients", "legacy-x", "input-methods", "general-desktop", "", "emacs", "tex", "internet-browser", "graphics", "technical-writing", "", "eclipse", "additional-devel", "server-platform-devel", "desktop-platform-devel", "development", "", "icelandic-support", "irish-support", "azerbaijani-support", "assamese-support", "afrikaans-support", "amazigh-support", "arabic-support", "albanian-support", "armenian-support", "italian-support", "inuktitut-support", "interlingua-support", "indonesian-support", "welsh-support", "ukrainian-support", "uzbek-support", "urdu-support", "estonian-support", "esperanto-support", "ethiopic-support", "dutch-support", "oriya-support", "kazakh-support", "kashmiri-support", "kashubian-support", "catalan-support", "kannada-support", "galician-support", "greek-support", "khmer-support", "kurdish-support", "croatian-support", "gujarati-support", "georgian-support", "gaelic-support", "xhosa-support", "coptic-support", "konkani-support", "sardinian-support", "sanskrit-support", "sindhi-support", "sinhala-support", "swedish-support", "spanish-support", "slovak-support", "slovenian-support", "swati-support", "swahili-support", "zulu-support", "serbian-support", "somali-support", "tsonga-support", "thai-support", "tagalog-support", "tajik-support", "tamil-support", "czech-support", "chichewa-support", "tibetan-support", "chhattisgarhi-support", "tswana-support", "tetum-support", "telugu-support", "danish-support", "turkmen-support", "turkish-support", "german-support", "southern-ndebele-support", "nepali-support", "norwegian-support", "hungarian-support", "basque-support", "punjabi-support", "hiligaynon-support", "hindi-support", "fijian-support", "filipino-support", "finnish-support", "faroese-support", "french-support", "friulian-support", "frisian-support", "brazilian-support", "bulgarian-support", "breton-support", "bhutanese-support", "hebrew-support", "vietnamese-support", "belarusian-support", "bengali-support", "venda-support", "persian-support", "portuguese-support", "polish-support", "maithili-support", "maori-support", "macedonian-support", "malagasy-support", "malayalam-support", "marathi-support", "maltese-support", "malay-support", "manx-support", "burmese-support", "mongolian-support", "lao-support", "latin-support", "latvian-support", "lithuanian-support", "luxembourgish-support", "kinyarwanda-support", "romanian-support", "occitan-support", "russian-support", "walloon-support", "chinese-support", "low-saxon-support", "northern-sotho-support", "southern-sotho-support", "japanese-support", "british-support", "korean-support", "upper-sorbian-support"]

$ports = ["amanda-client","bacula","bacula-client","dns","ftp","ipsec","nfs","openvpn","radius","cluster-suite","ssh","imaps","pop3s","samba","samba-client","tftp","tftp-client","http","ipp-client","ipp","mdns","smtp","libvirt","libvirt-tls","https"]



class Foo
  def main
    input = CGI.new
    print "Content-Type: text/html\n\n"
    print "<html><body>inputdata= "
    print "<pre>"
    input.each{|x|
      p x
    }
    print "<pre>"
#    c = ""
    print "<br><br><br><br><br>"
    c = self.parse(input)
    c += self.parse2(input)
    c += self.parse3(input)
    self.output(c)
    print "</body></html>"
  end
  def parse(input)
    config ="#version RHEL6
text
install
url --url http://192.168.56.254/rhel6
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
    
    fw  = ""
    if input['firewall'] == "enabled" then
      fw = "firewall --enabled"
      port = $ports
      port.each{|p|
        s = "fw." + p
        if input[s] then
          fw += " --" + p 
        end
      }

    elsif input['firewall'] == "disabled" then
      fw = "firewall --disabled"
    end
    fw += "\n"
    config += fw

    return config
  end


  def parse2(input)
    #disk layout
    config =""
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
  def output(config)
    print "<pre>"
    puts config
    print "</pre>"
    f = File.open("tmp/ks.cfg","w")
    f.puts(config)
  end

end  


f = Foo.new
f.main
