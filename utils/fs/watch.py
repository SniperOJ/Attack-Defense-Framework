#!/usr/bin/env python
# encoding:utf-8

import sys
import pyinotify
import os
import time

def detect_waf(pathname):
    try:
        with open(pathname) as f:
            content = f.read()
            black_list = ["<?", "<%"]
            black_list += ['eval', 'assert']
            black_list += ['passthru', 'exec', 'system', 'shell_exec', 'popen', 'proc_open']
            black_list += ['hightlight_file', 'show_source', 'php_strip_whitespace', 'file_get_contents', 'readfile', 'file', 'fopen', 'fread', 'include', 'include_once', 'require', 'require_once', 'fread', 'fgets', 'fpassthru', 'fgetcsv', 'fgetss', 'fscanf', 'parse_ini_file']
            black_list += ['glob', 'opendir', 'dir', 'readdir', 'scandir']
            FLAG = False
            for black in black_list:
                if black in content:
                    print "[!] Dangerous php script! (%s)" % (black)
                    print "[*] Content : "
                    print content.rstrip("\n")
                    FLAG = True
                    break
            if FLAG:
                target_path = "webshells/%s.log" % (time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())))
                print "[+] Detect webshell , moving from %s to %s" % (pathname, target_path)
                os.rename(pathname, target_path)
    except Exception as e:
        print "[-] %s" % (str(e))

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        if event.dir:
            print "Create Directory : %s" % (event.pathname)
        else:
            print "Create File : %s" % (event.pathname)

    def process_IN_DELETE(self, event):
        if event.dir:
            print "Delete Directory : %s" % (event.pathname)
        else:
            print "Delete File : %s" % (event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        if event.dir:
            print "Close Writable Directory : %s" % (event.pathname)
        else:
            print "Close Writable File : %s" % (event.pathname)
            detect_waf(event.pathname)

def main():
    if len(sys.argv) != 2:
        print "Usage : "
        print "\tpython %s [PATH]" % (sys.argv[0])
        exit(1)
    path = sys.argv[1]
    wm = pyinotify.WatchManager()
    wm.add_watch(path, pyinotify.ALL_EVENTS, rec=True)
    eh = EventHandler()
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == "__main__":
    main()
