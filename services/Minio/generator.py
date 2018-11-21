# -*- coding: utf-8 -*-

import configparser
import os
import sys


config = configparser.ConfigParser()
config.read('../config.ini')

service = "minio"

data = open("docker-compose.yml.example").read()
data = data.replace("__PORT__", config.get(service.lower(), "port"))
data = data.replace("__ACCESS_KEY__", config.get(service.lower(), "access"))
data = data.replace("__SECRET_KEY__", config.get(service.lower(), "secret"))
with open("docker-compose.yml", "w") as f:
    f.write(data)
