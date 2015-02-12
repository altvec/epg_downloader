#!/usr/bin/env python
# -*- conding: utf8 -*-

import re
import os
import sys
import ConfigParser
import urllib2
import xml.etree.ElementTree as ET
import subprocess
from time import strftime


def main():
    config = ConfigParser.RawConfigParser()
    try:
        config.readfp(open(r'settings.conf'))
    except IOError as e:
        print("Can't find settings.conf! Please create it")
        print("I/O error ({0}): {1}".format(e.errno, e.strerror))
        sys.exit(1)

    try:
        username = config.get('Main', 'username')
        password = config.get('Main', 'password')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
        print(e)
        print("Error in your settings.conf file:")
        sys.exit(1)

    out_dir = "files/"
    if not os.path.exists(os.path.dirname(out_dir)):
        os.makedirs(os.path.dirname(out_dir))

    url = 'http://xmltv.s-tv.ru/pers/{0}/index.php?pass={1}'.format(username,
                                                                    password)

    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print(e)
        print("Probably wrong username and/or password. Check settings.conf")
        sys.exit(1)

    xml_doc = response.read()

    # Here we parse the text in 'xml_doc' as a string, which creates an
    # Element, and then create an ElementTree using that Element.
    tree = ET.ElementTree(ET.fromstring(xml_doc))
    root = tree.getroot()
    procs = []
    channels = len(root)
    print("Downloading EPG for {0} channels. Please wait...".format(channels))

    for child in root:
        channel_src = re.sub('&sh=.*', '', child.attrib['src'])
        channel_id = child.attrib['channel_id']
        try:
            procs.append(subprocess.Popen(['/usr/bin/curl', '-s', '-o',
                                           out_dir + "/" +
                                           strftime("%Y-%m-%d_%H-%M-%S_") +
                                           channel_id + ".xml", channel_src]))
        except OSError as e:
            print("Looks like there is no curl installed in your system :(")
            sys.exit(1)

    for proc in procs:
        proc.wait()

    print("All done. Have a nice day!")


if __name__ == "__main__":
    main()
