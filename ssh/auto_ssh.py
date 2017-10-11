#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import time
import random
import hashlib
import string

timeout = 3

def login_with_password(host, port, username, password):
    # login via password
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, port=port, username=username, password=password, timeout=timeout)
        return (True, ssh)
    except Exception as e:
        return (False, str(e))


def login_with_key(host, port, username, key_file):
    # login via key
    private_key = paramiko.RSAKey._from_private_key_file(key_file)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, port=port, username=username, key=private_key, timeout=timeout)
        return (True, ssh)
    except Exception as e:
        return (False, str(e))

def exec_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return (stdin, stdout, stderr)

def exec_command_print(ssh, command):
    stdin, stdout, stderr = exec_command(ssh, command)
    print "-" * 0x10 + " STDOUT " + "-" * 0x10
    print stdout.read()
    print "-" * 0x10 + " STDERR " + "-" * 0x10
    print stderr.read()
    return (stdin, stdout, stderr)

def check_root(ssh):
    stdin, stdout, stderr = exec_command(ssh, "uname")
    result = stdout.read()
    return ("uid=0" in result, result)


def change_password(ssh, old_password, new_password):
    is_root = check_root(ssh)
    if is_root[0]:
        print "[+] Root user detected! (%s)" % (is_root[1])
        stdin, stdout, stderr = exec_command(ssh, "passwd")
        stdin.write("%s\n" % (new_password))
        stdin.write("%s\n" % (new_password))
        print "-" * 0x10 + " STDOUT " + "-" * 0x10
        print stdout.read()[:-1]
        print "-" * 0x10 + " STDERR " + "-" * 0x10
        error_message = stderr.read()[:-1]
        print error_message
        if "success" in error_message:
            return True
        else:
            return False
    else:
        print "[+] Not a root user! (%s)" % (is_root[1])
        stdin, stdout, stderr = exec_command(ssh, "passwd")
        stdin.write("%s\n" % (old_password))
        stdin.write("%s\n" % (new_password))
        stdin.write("%s\n" % (new_password))
        print "-" * 0x10 + " STDOUT " + "-" * 0x10
        print stdout.read()[:-1]
        print "-" * 0x10 + " STDERR " + "-" * 0x10
        error_message = stderr.read()[:-1]
        print error_message
        if "success" in error_message:
            return True
        else:
            return False

def md5(content):
    return hashlib.md5(content).hexdigest()

def random_string(length):
    random_range = string.letters + string.digits
    result = ""
    for i in range(length):
        result += random.choice(random_range)
    return result

def auto_change_password_with_password(target):
    print "-" * 32
    host = target[0]
    port = int(target[1])
    username = target[2]
    password = target[3]
    salt = random_string(32)
    new_password = md5("%s:%d:%s:%s:%s" % (host, port, username, password, salt))

    print "Host : %s" % (host)
    print "Port : %s" % (port)
    print "User : %s" % (username)
    print "Pass : %s" % (password)
    print "NewP : %s" % (new_password)
    print "Trying to login..."
    result = login_with_password(host, port, username, password)
    if result[0]:
        ssh = result[1]
        print "[+] Login success!"
        print "[+] Trying to change password [%s] => [%s]" % (password, new_password)
        change_password(ssh, password, new_password)
        with open("ssh.log", "a+") as f:
            content = "%s:%s@%s:%d => %s\n" % (username, password, host, port, new_password)
            f.write(content)
        print "[+] Closing conneciton..."
        ssh.close()
        print "[+] Connection closed!"
    else:
        print "[-] Login error!"
        print "[-] %s" % (result[1])

def auto_change_password_with_key(target):
    print "-" * 32
    host = target[0]
    port = int(target[1])
    username = target[2]
    key_path = target[3]
    salt = random_string(32)
    new_password = md5("%s:%d:%s:%s" % (host, port, username, salt))

    print "Host : %s" % (host)
    print "Port : %s" % (port)
    print "User : %s" % (username)
    print "File : %s" % (key_path)
    print "NewP : %s" % (new_password)
    print "Trying to login..."
    result = login_with_key(host, port, username, key_path)
    if result[0]:
        ssh = result[1]
        print "[+] Login success!"
        #print "[+] Trying to change password [%s] => [%s]" % (password, new_password)
        #change_password(ssh, password, new_password)
        #with open("ssh.log", "a+") as f:
        #    content = "%s:%s@%s:%d => %s\n" % (username, password, host, port, new_password)
        #    f.write(content)
        #print "[+] Closing conneciton..."
        ssh.close()
        #print "[+] Connection closed!"
    else:
        print "[-] Login error!"
        print "[-] %s" % (result[1])

def main():
    '''
    with open("ssh_targets_with_password") as f:
        for line in f:
            data = line.replace("\n", "").split(" ")
            auto_change_password_with_password(data)
            '''
    with open("ssh_targets_with_key") as f:
        for line in f:
            data = line.replace("\n", "").split(" ")
            auto_change_password_with_key(data)


if __name__ == "__main__":
    main()

