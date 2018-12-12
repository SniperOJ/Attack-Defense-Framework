# -*- coding: utf-8 -*-

import configparser
import os
import sys


config = configparser.ConfigParser()
config.read('../config.ini')

service = "nextcloud"

data = open("docker-compose.yml.example").read()
data = data.replace("__HOST__", config.get(service.lower(), "host"))
data = data.replace("__PORT__", config.get(service.lower(), "port"))
with open("docker-compose.yml", "w") as f:
    f.write(data)
