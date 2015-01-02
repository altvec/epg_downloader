#!/usr/bin/env python

import re
import os
import ConfigParser
import urllib2
import xml.etree.ElementTree as ET
import subprocess

config = ConfigParser.RawConfigParser()
config.readfp(open(r'../settings.conf'))
username = config.get('Main', 'username')
password = config.get('Main', 'password')

out_path = "./files/"
if not os.path.exists(os.path.dirname(out_path)):
    os.makedirs(os.path.dirname(out_path))

base_url = 'http://xmltv.s-tv.ru/pers/%s/index.php?pass=%s' % (username,
        password)

file = "base_source.xml"
response = urllib2.urlopen(base_url)
with open(file, 'wb') as f:
    f.write(response.read())

tree = ET.parse(file)
root = tree.getroot()
procs = []
for child in root:
    channel_src = re.sub('&sh=.*', '', child.attrib['src'])
    channel_id = child.attrib['channel_id']
    procs.append(subprocess.Popen(['/usr/bin/curl', '-s', '-o',
        out_path+"/"+channel_id+".xml", channel_src]))
for proc in procs:
    proc.wait()

os.remove(file)
