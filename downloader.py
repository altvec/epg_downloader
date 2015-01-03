#!/usr/bin/env python
# -*- conding: utf8 -*-

import re
import os
import ConfigParser
import urllib2
import xml.etree.ElementTree as ET
import subprocess

config = ConfigParser.RawConfigParser()
config.readfp(open(r'settings.conf'))
username = config.get('Main', 'username')
password = config.get('Main', 'password')

out_dir = "files/"
if not os.path.exists(os.path.dirname(out_dir)):
    os.makedirs(os.path.dirname(out_dir))

url = 'http://xmltv.s-tv.ru/pers/%s/index.php?pass=%s' % (username, password)

file = "stv.xml"
response = urllib2.urlopen(url)
with open(file, 'wb') as f:
    f.write(response.read())

tree = ET.parse(file)
root = tree.getroot()
procs = []

print "Downloading EPG files for %s channels. Please wait a bit" % (len(root))

for child in root:
    channel_src = re.sub('&sh=.*', '', child.attrib['src'])
    channel_id = child.attrib['channel_id']
    procs.append(subprocess.Popen(['/usr/bin/curl', '-s', '-o',
                                  out_dir+"/"+channel_id+".xml", channel_src]))
for proc in procs:
    proc.wait()

os.remove(file)
print "All done. Have a nice day!"
