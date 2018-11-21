# -*- coding: utf-8 -*-

import configparser


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

generate("sirius")
generate("submittor")
generate("platypus")