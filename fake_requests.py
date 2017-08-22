#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import threading

from core.obfs.fake_payloads import *
from core.obfs.get_arg import *

timeout = 1

def send_http(request):
    print "[+] Sending : [%s]" % (request.url)
    prepared = request.prepare()
    session = requests.Session()
    session.send(prepared, timeout=timeout)

def handle_get(url, root, flag_path):
    all_requests = []
    http_get = get_all(root, "_GET")
    plain_payloads = get_fake_plain_payloads(flag_path)
    base64_payloads = get_fake_base64_payloads(flag_path)
    for item in http_get:
        path = item[0]
        args = item[1]
        for arg in args:
            for payload in plain_payloads:
                new_url = "%s%s?%s=%s" % (url, path[len("./"):], arg[len("$_GET['"):-len("']")], payload)
                request = requests.Request("GET", new_url)
                all_requests.append(request)
            for payload in base64_payloads:
                new_url = "%s%s?%s=%s" % (url, path[len("./"):], arg[len("$_GET['"):-len("']")], payload)
                request = requests.Request("GET", new_url)
                all_requests.append(request)
    for request in all_requests:
        handle_single_http(request)

def handle_single_http(request):
    send_http(request)

def handle_post(url, root, flag_path):
    all_requests = []
    http_get = get_all(root, "_POST")
    plain_payloads = get_fake_plain_payloads(flag_path)
    base64_payloads = get_fake_base64_payloads(flag_path)
    for item in http_get:
        path = item[0]
        args = item[1]
        for arg in args:
            for payload in plain_payloads:
                new_url = "%s%s" % (url, path[len("./"):])
                request = requests.Request("POST", new_url)
                request.data = {
                    arg[len("$_POST['"):-len("']")]:payload
                }
                all_requests.append(request)
            for payload in base64_payloads:
                new_url = "%s%s" % (url, path[len("./"):])
                request = requests.Request("POST", new_url)
                request.data = {
                    arg[len("$_POST['"):-len("']")]:payload
                }
                all_requests.append(request)
    for request in all_requests:
        handle_single_http(request)

def handle_cookie(url, root, flag_path):
    all_requests = []
    http_get = get_all(root, "_COOKIE")
    plain_payloads = get_fake_plain_payloads(flag_path)
    base64_payloads = get_fake_base64_payloads(flag_path)
    for item in http_get:
        path = item[0]
        args = item[1]
        for arg in args:
            for payload in plain_payloads:
                new_url = "%s%s" % (url, path[len("./"):])
                request = requests.Request("GET", new_url)
                request.cookies = {
                    arg[len("$_COOKIE['"):-len("']")]:payload
                }
                all_requests.append(request)
            for payload in base64_payloads:
                new_url = "%s%s" % (url, path[len("./"):])
                request = requests.Request("GET", new_url)
                request.cookies = {
                    arg[len("$_COOKIE['"):-len("']")]:payload
                }
                all_requests.append(request)
    for request in all_requests:
        handle_single_http(request)

def main():
    url = "http://127.0.0.1/"
    root = "./test"
    flag_path = "/home/web/flag/flag"
    handle_get(url, root, flag_path)
    handle_post(url, root, flag_path)
    handle_cookie(url, root, flag_path)

if __name__ == "__main__":
    main()
