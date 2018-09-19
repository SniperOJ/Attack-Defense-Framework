#!/usr/bin/env python

import requests
import ConfigParser
import json

config = ConfigParser.ConfigParser()
config.read('./config.ini')  

def query(model):
    url = "http://%s:%s/api/%s/" % (
        config.get("sirius", "host"), 
        config.get("sirius", "port"), 
        model
    )
    return json.loads(requests.get(url, headers={
        'Authorization': 'Bearer %s' % (config.get("sirius", "token")), 
    }).content)

def main():
    print query("log")
    print query("target")

if __name__ == "__main__":
    main()
