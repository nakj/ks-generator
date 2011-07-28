#!/usr/bin/env ruby -Ku
# -*- coding: utf-8 -*-

$file = "/home/jin/rpmbuild/BUILD/anaconda-13.21.82/lang-table"
$pofile = "/home/jin/rpmbuild/BUILD/anaconda-13.21.82/po/ja.po"


def list
  ret = Array.new
  f = open($file)
  f.each{|x|
    x.strip!
    y = x.split(/\s*\t\s*/)
    a = [y[0],y[3],y[4],y[5]]
    #printf("%s\t%s\t%s\t%s\n",y[0],y[3],y[4],y[5])
    ret << a
  }
  return ret
end

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
def retary
  a = list
  b = parsepo
  c = []
  a.each{|x|
    d = []
    d[1]= x[1]
    d[2]= x[2]
    d[3]= x[3]
    d[0] = b.assoc(x[0])[1]
    c << d
  }
  return c
end


a = retary
b = []
a.each{|x|
  b << x[3]
}
#p b
#b = a.sort{|a,b| a[3] <=> b[3] }

b.uniq.sort.each{|x|
#  printf("<option value=\"%s\">%s</option>\n",x[3],x[3])
  printf("<option value=\"%s\">%s</option>\n",x,x)

  
}

#<option value="en_US.UTF-8">英語</option>
