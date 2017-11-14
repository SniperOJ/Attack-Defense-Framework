#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

def get_content(path):
    return open(path).read()

def find_arg(content, arg):
    p = re.compile(r'\$' + arg + '\[[\'"]\w+[\'"]\]')
    return list(set(p.findall(content)))

def get_all(root, arg):
    all = []
    result = os.walk(root)
    for path,d,filelist in result:
        for file in filelist:
            if file.endswith(".php"):
                full_path = path + "/" + file
                content = get_content(full_path)
                all.append(("/" + file, find_arg(content, arg)))
    return all

def main():
    root = "."
    print get_all(root, "_GET")
    print get_all(root, "_POST")
    print get_all(root, "_COOKIE")

if __name__ == "__main__":
    # main()
    get_all("/etc", "_GET")
