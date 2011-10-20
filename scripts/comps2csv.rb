#!/usr/bin/env ruby -Ku
# -*- coding: utf-8 -*-

=begin
RHEL6.0クローンのSL6で動作確認しています。
0. 準備
   必要なパッケージをインストール
   # yum groupinstall "Development Tools"
   # yum install rubygems ruby-devel
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
      if g[1] == nil then
        g <<  el.at("name").inner_text
      end
      el.search("description").each{|d|
        if d.attributes['xml:lang'] == "ja"
          g << d.inner_text.toutf8
        end
      }
      if g[2] == nil then
        g << el.at("description").inner_text
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
        printf('"%s","%s","%s"',x[0],x[1],x[2])
=begin
        printf('<tr><td><input type="checkbox" name="pkg.%s" value="true">',x[0])
        printf(' %s',x[1])
        printf('</td>')
        printf('<td>%s</td></tr>',x[2])
=end
        printf("\n")
      else
        print '"",'
=begin
        printf('<tr><th>%s</th></tr>',x)
=end
        printf("\n")
      end
    }
  end
end


if $0 == __FILE__ then
  prm = ParamSheet.new
  prm.main(ARGV[0])
end
