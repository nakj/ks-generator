#!/usr/bin/ruby -Ku
# -*- coding: utf-8 -*-
require "cgi-lib"
require "kconv"
require "rubygems"
require "hpricot"

print "Content-Type: text/html\n\n"

$core="/var/pxe/rhel5/Server/repodata/comps-rhel5-server-core.xml"

class ParamSheet
  def groups(doc)
    ret = Array.new
    doc.search("group").each{|el|
      g = Array.new
      g << el.at("id").inner_text
      el.search("name").each {|n|
        if  n.attributes['xml:lang'] == "ja"
          g << n.inner_text.toutf8
        end
      }
      if g[1] == nil then
        g <<  el.at("name").inner_text
      end
      el.search("description").each{|d|
        if d.attributes['xml:lang'] == "ja"
          g << d.inner_text.toutf8
        end
      }
      if g[2] == nil then
        d = el.at("description")
        unless d == nil then
          g << d.inner_text
          else
          g << ""
        end

      end

      ret << g
    }
    return ret
  end
  def ctg(file)
    ret = Array.new
    doc = Hpricot::XML(open(file))
    gl = groups(doc)

    doc.search("category").each{|cat|
      ary = Array.new

      next if cat.at("id").inner_text == "language-support"

      cat.search("name").each{|name|
        if name.attributes["xml:lang"] == "ja"
          ret << name.inner_text
        end    
      }

      cat.search("groupid").each{|gid|
        grp = gl.assoc(gid.inner_text)
        unless grp == nil then
          ary << grp
        end
      }
      ret = ret + ary.sort!{|a,b| a[1] <=> b[1]}
    }
    return ret
  end
  def main(file)
    r = self.ctg(file)
    printf("<table border=1>")

    r.each{|x|
      if x.class == Array then
#        printf('"%s","%s","%s"',x[0],x[1],x[2])

        printf('<tr><td><input type="checkbox" name="pkg.%s" value="true">',x[0])
        printf(' %s',x[1])
        printf('</td>')
        printf('<td>%s</td></tr>',x[2])

        printf("\n")
      else
#        print '"",'

        printf('<tr><th>%s</th></tr>',x)

        printf("\n")
      end
    }
  end
end


if $0 == __FILE__ then
  prm = ParamSheet.new
  prm.main($core)
end



