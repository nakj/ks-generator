#!/usr/bin/env ruby -Ku
# -*- coding: utf-8 -*-

=begin
RHEL6.0クローンのSL6で動作確認しています。
0. 準備
   必要なパッケージをインストール
   # yum install rubygems libxml2 libxml2-devel libxslt-devel libxslt
   # yum groupinstall "Development Tools"
   gem ライブラリをインストール
   # gem install hpricot
1.実行
   引数にxmlファイルを渡します。
   # ruby test.rb /mnt/repodata/comps.xml

=end

require "kconv"
require "rubygems"
require "hpricot"
#file = "greped_grouplist.txt"
#f = open("comps.xml")


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
      el.search("description").each{|d|
        if d.attributes['xml:lang'] == "ja"
          g << d.inner_text.toutf8
        end
      }
      ret << g
    }
    return ret
  end
  def ctg(file)
    ret = Array.new
    doc = Hpricot::XML(open(file))
    gl = self.groups(doc)

    doc.search("category").each{|cat|
      ary = Array.new
      cat.search("name").each{|name|
        if name.attributes["xml:lang"] == "ja"
          ret << name.inner_text
        end    
      }

      cat.search("groupid").each{|gid|
        grp = gl.assoc(gid.inner_text)
        ary << grp
      }
      ret = ret + ary.sort!{|a,b| a[1] <=> b[1]}
    }
    return ret
  end
  def main(file)
    r = self.ctg(file)
    r.each{|x|
      if x.class == Array then
       # printf('"%s","%s","%s"',x[0],x[1],x[2])

        printf('<tr><td><input type="checkbox" name="pkg.%s" value="true">',x[0])
        printf(' %s',x[1])
        printf('</td>')
        printf('<td>%s</td></tr>',x[2])

        printf("\n")
      else
        #print '"",'

        printf('<tr><th colspan=3 align="left">%s</th></tr>',x)

        printf("\n")
      end
    }
  end
  def main2(file)
    doc =Hpricot::XML(open(file))

    gl = self.groups(doc)

    doc.search("category").each{|x|


      if x.at("id").inner_text == "language-support" then
        x.search("groupid").each{|y|
          z = gl.assoc(y.inner_text)
          printf('<option value="pkg.%s">%s</option>',z[0],z[1])
          print "\n"

        }
      end

    }


  end
end


if $0 == __FILE__ then
  prm = ParamSheet.new
  prm.main2(ARGV[0])
end
