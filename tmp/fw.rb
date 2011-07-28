#!/usr/bin/ruby -Ku

$file = "/home/jin/rpmbuild/BUILD/system-config-firewall-1.2.27/src/fw_services.py"
$pofile = "/home/jin/rpmbuild/BUILD/system-config-firewall-1.2.27/po/ja.po"

def parsepo
  f = open($pofile)
  str = ""
  f.readlines.each{|x|
    str += x
  }
  b = []
  str.split(/\n\n/).each{|x|

    y = x.split(/\n/)
    y.shift
    y[0] = y[0].match(/".*"/).to_s.gsub(/"/,"")
    y[1] = y[1].match(/".*"/).to_s.gsub(/"/,"")
    b << y
  }
  return b
end
def parsepo2
  f = open($pofile)
  str = ""
  f.readlines.each{|x|
    str += x
  }
  b = []
  str.split(/\#/).each{|x|
    y = x.split(/\n/)
    y.shift
    unless y.size == 0 then
    y[0] = y[0].match(/".*"/).to_s.gsub(/"/,"")
    y[1] = y[1].match(/".*"/).to_s.gsub(/"/,"")
      b << y
    end
    
  }
  return b
end


def list
  ret = []
  f = open($file)
  f.readlines.each{|x|
     x.strip!
    r = []
    if x.match(/^_Service/) then
       r[0] = x.split(/\s*,\s*/)[0].gsub(/^_Service\(\"/,"").gsub(/\"$/,"")
       r[1] =x.split(/\s*,\s*/)[1].gsub(/^_\(\"/,"").gsub(/\"\)$/,"")
     ret <<  r
    end
  }
  return ret
end
b = parsepo2

 a = list

a.map{|x|
   x[0] 
   x[1] = b.assoc(x[1])[1]
}
p a
a.sort{|a,b| a[1] <=> b[1]}.each{|x|
  printf('<tr><td><input type="checkbox" name="fw.%s" value="true">%s</input></td></tr>', x[0],x[1])
  printf("\n")
}
