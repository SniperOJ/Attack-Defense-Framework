#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko

def login_with_password(host, port, username, password):
    # login via password
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, port=port, username=username, password=password)
        return (True, ssh)
    except Exception as e:
        return (False, str(e))


def login_with_key(host, port, username, key_file):
    # login via key
    private_key = paramiko.RSAKey._from_private_key_file(key_file)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host, port=port, username=username, key=private_key)
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

def main():
    # paramiko.util.log_to_file('paramiko.log')
    host = "127.0.0.1"
    port = 22
    username = "root"
    password = ""
    command = "id"
    result = login_with_password(host, port, username, password)
    if result[0]:
        ssh = result[1]
        print "[+] Login success!"
        exec_command_print(ssh, command)
    else:
        print "[-] Login error!"
        print "[-] %s" % (result[1])

if __name__ == "__main__":
    main()

