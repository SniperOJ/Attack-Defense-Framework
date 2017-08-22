# -*- coding: utf-8 -*-

import get_arg
import fake_payloads

def main():
    url = "http://127.0.0.1/"
    root = "./web"
    flag_path = "/home/web/flag/flag"
    http_get = get_arg.get_all(root, "_GET")
    plain_payloads = fake_payloads.get_fake_plain_payloads(flag_path)
    base64_payloads = fake_payloads.get_fake_base64_payloads(flag_path)
    for item in http_get:
        path = item[0]
        args = item[1]
        for arg in args:
            for payload in plain_payloads:
                print "%s%s?%s=%s" % (url, path[len("./"):], arg[len("$_GET['"):-len("']")], payload)
            for payload in base64_payloads:
                print "%s%s?%s=%s" % (url, path[len("./"):], arg[len("$_GET['"):-len("']")], payload)


if __name__ == "__main__":
    main()
