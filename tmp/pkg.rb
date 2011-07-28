#!/usr/bin/ruby -Ku
# -*- coding: utf-8 -*-



def list 
  f = open("rhel6.csv")
  a = []
  
  f.readlines.each{|x|
    a <<  x.split(/\s*,\s*/)[0].gsub(/"/,"")
  }
  
  return a
end


p  list
