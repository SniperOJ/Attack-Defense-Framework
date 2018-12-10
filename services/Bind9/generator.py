# -*- coding: utf-8 -*-

import configparser
import os
import sys

host = sys.argv[1]
data = open("db.lilac.com.example").read()
with open("db.lilac.com", "w") as f:
    data = data.replace("__HOST__", host)
    f.write(data)

os.system("cp db.lilac.com /etc/bind/")
os.system("cp named.conf.default-zones /etc/bind/")
os.system("cp named.conf.options /etc/bind/")
os.system("service bind9 restart")
