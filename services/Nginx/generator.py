# -*- coding: utf-8 -*-

import configparser
import os

def generate(service):
    config = configparser.ConfigParser()
    config.read('../config.ini')
    template = open("sites-available/template").read()
    with open("sites-available/%s" % (service.lower()), "w") as f:
        data = template
        data = data.replace("__HOST__", config.get(service.lower(), "host"))
        data = data.replace("__PORT__", config.get(service.lower(), "port"))
        data = data.replace("__NAME__", service.lower())
        f.write(data)

def auth():
    config = configparser.ConfigParser()
    config.read('../config.ini')
    username = config.get("nginx", "username")
    password = config.get("nginx", "password")
    command = 'printf "%s:$(openssl passwd -crypt %s)\n" > ./auth/basic' % (username, password)
    os.system(command)

generate("sirius")
generate("submittor")
generate("platypus")
auth()
