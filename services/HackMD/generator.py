# -*- coding: utf-8 -*-

import configparser
import os
import sys


config = configparser.ConfigParser()
config.read('../config.ini')

suffix = "lilac.com"
service = "hackmd"

data = open("docker-compose.yml.example").read()
data = data.replace("__HOSTNAME__", "%s.%s" % (service, suffix))
data = data.replace("__HOST__", config.get(service.lower(), "host"))
data = data.replace("__PORT__", config.get(service.lower(), "port"))
data = data.replace("__MINIO_ENDPOINT__", "%s.%s" % ("minio", suffix))
data = data.replace("__ACCESS_KEY__", config.get("minio", "access"))
data = data.replace("__SECRET_KEY__", config.get("minio", "secret"))
with open("docker-compose.yml", "w") as f:
    f.write(data)
