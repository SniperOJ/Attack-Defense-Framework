# -*- coding: utf-8 -*-

import configparser
import os
import sys

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
        data += "%s %s\n" % (config.get(service.lower(), "host"), "%s.%s" % (service.lower(), suffix))
    with open("hosts", "w") as f:
        f.write(data)

def nginx(services):
    config = configparser.ConfigParser()
    config.read('../config.ini')
    for service in services:
        print("./sites-available/%s.example" % (service))
        if os.path.isfile("./sites-available/%s.example" % (service)):
            print "example file for %s found" % (service)
            template = open("sites-available/%s.example" % (service)).read()
        else:
            template = open("sites-available/default.example").read()
        with open("sites-available/%s" % (service.lower()), "w") as f:
            data = template
            data = data.replace("__HOSTNAME__", "%s.%s" % (service.lower(), suffix))
            data = data.replace("__HOST__", config.get(service.lower(), "host"))
            data = data.replace("__PORT__", config.get(service.lower(), "port"))
            data = data.replace("__NAME__", service.lower())
            f.write(data)

def setup(services):
    # Basic auth
    os.system("mkdir /etc/nginx/auth/")
    os.system("cp ./nginx.conf /etc/nginx/nginx.conf")
    os.system("cp ./auth/basic /etc/nginx/auth/basic")
    for service in services:
        os.system("cp ./sites-available/%s /etc/nginx/sites-available/" % service)
        os.system("ln -s /etc/nginx/sites-available/%s /etc/nginx/sites-enabled/%s" % (service, service))
    os.system("service nginx restart")
    os.system("cat hosts /etc/hosts | sort -nr | uniq > /tmp/hosts && mv /tmp/hosts /etc/hosts")
    # TODO: IDarling port should obtained from config.ini
    os.system("cp -r ./tcpconf.d /etc/nginx/")

services = [
    "sirius",
    "submittor",
    "platypus",
    "chat",
    "hackmd",
    "minio",
    "wiki",
    "nextcloud",
]

if len(sys.argv) <= 1:
    auth()
    hosts(services)
    nginx(services)
    setup(services)
else:
    command = sys.argv[1].lower()
    if command == "auth":
        auth()
    elif command == "hosts":
        hosts(services)
    elif command == "nginx":
        nginx(services)
    elif command == "setup":
        setup(services)
    else:
        print "No such command"

