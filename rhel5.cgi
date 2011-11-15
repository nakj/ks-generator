#!/usr/bin/ruby -Ku
# -*- coding: utf-8 -*-
require "cgi-lib"


print "Content-Type: text/html\n\n"

$core="/var/pxe/rhel5/Server/repodata/comps-rhel5-server-core.xml"

f = open($core)

p f.readlines
