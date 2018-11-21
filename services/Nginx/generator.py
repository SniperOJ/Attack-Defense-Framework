# -*- coding: utf-8 -*-

import configparser
import os

suffix = "lilac.com"

def auth():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    username = config.get("nginx", "username")
    password = config.get("nginx", "password")
    command = 'printf "%s:$(openssl passwd -crypt %s)\n" > ./auth/basic' % (username, password)
    os.system(command)

def hosts(services):
    config = configparser.ConfigParser()
    config.read('../config.ini')
    data = ""
    for service in services:
        data += "%s\t%s" % (config.get(service.lower(), "host"), "%s.%s" % (service.lower(), suffix))
    with open("hosts", "w") as f:
        f.write(data)

def nginx(services):
    config = configparser.ConfigParser()
    config.read('../config.ini')
    template = open("sites-available/template").read()
    for service in services:
        with open("sites-available/%s" % (service.lower()), "w") as f:
            data = template
            data = data.replace("__HOSTNAME__", "%s.%s" % (service.lower(), suffix))
            data = data.replace("__HOST__", config.get(service.lower(), "host"))
            data = data.replace("__PORT__", config.get(service.lower(), "port"))
            data = data.replace("__NAME__", service.lower())
            f.write(data)

services = [
    "sirius",
    "submittor",
    "platypus",
]

auth()
hosts(services)
nginx(services)
