#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_lastest_password(log_file):
    results = {}
    with open(log_file) as f:
        for line in f:
            data = line.replace("\n", "").split(" => ")
            key = data[0]
            value = data[1]
            if key in results.keys():
                print "[+] Update : %s [%s] => [%s]" % (key, results[key], value)
            else:
                print "[+] Detact : %s [%s]" % (key, value)
            results[key] = value
    return results

def main():
    log_file = "ssh.log"
    get_lastest_password(log_file)

if __name__ == "__main__":
    main()

