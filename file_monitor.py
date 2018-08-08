#!/usr/bin/env python
# encoding:utf-8

import sys
import pyinotify
import logging
import time
from collections import deque
import threading
import uuid
import os


WORKER_NUMBER = 2
WORKER_WAIT_TIME = 5
debug_mode = True
logging.basicConfig(filename='pyinotify.log', level=logging.INFO)
jobs = deque([])


def d(data):
    print "[DEBUG] %s" % (data)


def e(data):
    print "[ERROR] %s" % (data)


def describe_content(content):
    # Assume that content does not contains \n
    if len(content) < 6:
        return content.strip()
    return (content.strip()[:3] + "..." + content.strip()[-3:])


def describe_time():
    return time.strftime('%Y-%m-%d.%H:%M:%S', time.localtime(time.time()))


def record_file_content(content, worker_id):
    record_file = "%s/%d.%s.%s.content" % (
        history_log_path,
        worker_id,
        uuid.uuid4(),
        describe_time(),
    )
    d("[*] Recording %s(%s)(%d lines) into %s" % (
        file,
        describe_content(content),
        len(content.split("\n")),
        record_file,
    ))
    with open(record_file, "a+") as f:
        f.write("%s\n" % content)
    return True


def create_new_job(content):
    # Jobs status:
    #   True: submitted and accepted by server
    #         It means that workers does not need to submit it anymore
    #   False: Other cases
    job = {
        "content": content,
        "status": False,
        "time": time.time(),
    }
    return job


def file_snapshot(file, worker_id):
    while True:
        try:
            job = jobs.popleft()
            if not job['status']:
                result = record_file_content(
                    job['content'],
                    worker_id
                )
                if result:
                    d("[+][%d] Content (%s) recorded" % (
                        worker_id,
                        describe_content(job['content']),
                    ))
                else:
                    d("[-][%d] Content (%s) *didn't* accepted" % (
                        worker_id,
                        describe_content(job['content']),
                    ))
                    # Add queue, waiting for resubmit
                    job['status'] = False
                    jobs.append(job)
        except Exception as e:
            d("[!] %s" % (e))
            time.sleep(WORKER_WAIT_TIME)


class EventHandler(pyinotify.ProcessEvent):
    def debug(self, event):
        if not debug_mode:
            return
        ts = time.strftime('%d-%H:%M:%S', time.localtime(time.time()))
        if event.dir:
            logging.info("[%s] %s" % (ts, event))
        else:
            logging.info("[%s] %s" % (ts, event))

    def process_IN_ACCESS(self, event):
        d("File has been accessed")
        self.debug(event)

    def process_IN_CLOSE_WRITE(self, event):
        '''
        File content modified
        # Everytime someone change the content of the target file
        # this function will be involved
        '''
        d("File content has been changed")
        self.debug(event)
        # Snapshot file content
        content = open(file).read()
        # Record file content to server
        # Actually add it to a queue, waiting for worker to submit
        jobs.append(create_new_job(content))

    def process_default(self, event):
        self.debug(event)


def start_workers():
    for i in range(WORKER_NUMBER):
        t = threading.Thread(target=file_snapshot, args=(file, i, ))
        t.daemon = True
        t.start()


def main():
    global file
    global history_log_path

    if len(sys.argv) != 3:
        print "Usage : "
        print "\tpython %s [FILE] [HISTORY_LOG_PATH]" % (sys.argv[0])
        exit(1)

    # Get params from cli
    file = sys.argv[1]
    history_log_path = sys.argv[2]

    if os.path.isdir(file):
        e("Can not monitor on a directory")
        return

    logging.info("Started at <%s>" % (describe_time()))

    # Record file content at first time
    jobs.append(create_new_job(open(file).read()))

    # Start workers to snapshot file to server
    start_workers()

    # Start pyinotify
    wm = pyinotify.WatchManager()
    wm.add_watch(file, pyinotify.ALL_EVENTS, rec=True)
    eh = EventHandler()
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()


if __name__ == "__main__":
    main()
