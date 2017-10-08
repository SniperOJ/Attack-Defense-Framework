#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import threading
import time
import random

from core.obfs.fake_payloads import *
from core.obfs.get_arg import *

timeout = 0.1

def send_http(request):
    prepared = request.prepare()
    session = requests.Session()
    try:
        session.send(prepared, timeout=timeout)
    except Exception as e:
        print e

def handle_single_http(request):
    send_http(request)

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
    return all_requests

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
    return all_requests

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
    return all_requests

def get_targets():
    targets = []
    with open("targets") as f:
        for line in f:
            host = line.split(":")[0]
            port = int(line.split(":")[1])
            targets.append((host, port))
    return targets

def main():
    flag_path = "/home/web/flag/flag"
    root = "./sources"
    round_time = 60
    all_requests = []
    targets = get_targets()
    for target in targets:
        print "-" * 32
        host = target[0]
        port = target[1]
        print "[+] Generating requests to fake %s:%d" % (host, port)
        url = "http://%s:%d/" % (host, port)
        print "[+] Requests number : [%d]" % (len(all_requests))
        all_requests += handle_get(url, root, flag_path)
        print "[+] Requests number : [%d]" % (len(all_requests))
        all_requests += handle_post(url, root, flag_path)
        print "[+] Requests number : [%d]" % (len(all_requests))
        all_requests += handle_cookie(url, root, flag_path)

    each_second = len(all_requests) / round_time
    print "[+] Each second should send %d requests" % (each_second)
    random.shuffle(all_requests)
    for request in all_requests:
        sleep_time = 1.0 / each_second
        print "[+] Sleeping %f seconds" % (sleep_time)
        time.sleep(sleep_time)
        print "[+] Sending http requests ..."
        print "%s => %s" % (request.method, request.url)
        thread = threading.Thread(target=handle_single_http, args=(request,))
        thread.start()
        thread.join()


if __name__ == "__main__":
    main()
