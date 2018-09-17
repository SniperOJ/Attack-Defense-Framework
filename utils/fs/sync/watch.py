# -*- coding: utf-8 -*-
import pyinotify
import paramiko
import threading
import time
import os
import sys
import glob
from collections import deque

# Worker configuration
WORKER_NUMBER = 1
WORKER_WAIT_TIME = 5
jobs = deque([])
# SSH configuration
hostname = "127.0.0.1"
port = 22
# Auth with user/pass
username = ""
password = ""


def d(data):
    print "[DEBUG] %s" % (data)


def e(data):
    print "[ERROR] %s" % (data)


def get_ssh_by_password(hostname, port, username, password):
    try:
        ssh_session = paramiko.SSHClient()
        ssh_session.load_system_host_keys()
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_session.connect(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            timeout=3,
        )
        return ssh_session
    except Exception as exception:
        e(repr(exception))
        return False


def get_ssh_by_public_key(host, port, username, private_key_file):
    try:
        ssh_session = paramiko.SSHClient()
        ssh_session.load_system_host_keys()
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey._from_private_key_file(private_key_file)
        ssh_session.connect(
            hostname=host,
            port=port,
            username=username,
            key=private_key,
            timeout=3,
        )
        return ssh_session
    except Exception as exception:
        e(repr(exception))
        return False


def get_sftp(ssh_session):
    if ssh_session:
        return ssh_session.open_sftp()
    return False


def create_job(event):
    job = {
        "event": event,
        "status": False,
    }
    return job


def get_remote_path(path):
    sub_path = path[path.index(src) + len(src):]
    return "%s%s" % (dst, sub_path)


def job_handler(sftp, job):
    try:
        event = job['event']
        # Handle init jobs first
        if isinstance(event, dict):
            if event['dir']:
                result = sftp.mkdir(
                    get_remote_path(event['file'])
                )
                d("[D] %s: %s" % (event, result))
            else:
                result = sftp.put(
                    event['file'],
                    get_remote_path(event['file'])
                )
                d("[F] %s: %s" % (event, result))
            return True
        # Create a directory
        if event.mask == pyinotify.IN_CREATE | pyinotify.IN_ISDIR:
            result = sftp.mkdir(get_remote_path(event.pathname))
            d("[D] %s: %s" % (event.maskname, result))
            d("[!] Stopping watcher")
            notifier.stop()
            os._exit(2)
        # Write a file
        elif event.mask == pyinotify.IN_CLOSE_WRITE:
            if not event.dir:
                result = sftp.put(
                    event.pathname,
                    get_remote_path(event.pathname)
                )
                d("[F] %s: %s" % (event.maskname, result))
        # Delete a file
        elif event.mask == pyinotify.IN_DELETE:
            if event.dir:
                result = sftp.remove(get_remote_path(event.pathname))
                d("[D] %s: %s" % (event.maskname, result))
            else:
                result = sftp.rmdir(get_remote_path(event.pathname))
                d("[F] %s: %s" % (event.maskname, result))
        # Rename
        elif event.mask == pyinotify.IN_MOVED_TO:
            result = sftp.rename(
                get_remote_path(event.src_pathname),
                get_remote_path(event.pathname)
            )
            d("%s: %s" % (event.maskname, result))
        else:
            # This case will never be executed
            e("Unknown event type: %s" % event.mask)
        return True
    except IOError as exception:
        e(repr(exception))
        return True
    except Exception as exception:
        e(repr(exception))
        return False


def worker_handler(worker_id):
    d("Worker [%d] started" % (worker_id))
    d("Worker [%d] connecting to server" % (worker_id))
    # TODO: change auth method
    sftp = get_sftp(get_ssh_by_password(
        hostname=hostname,
        port=port,
        username=username,
        password=password,
    ))
    if not sftp:
        d("Worker [%d] can not connect to server, exiting" % (worker_id))
        return
    d("Worker [%d] connected" % (worker_id))
    while True:
        try:
            job = jobs.popleft()
            if not job['status']:
                d("[+] Worker [%d] start handling job [%s]" % (
                    worker_id,
                    job,
                ))
                if job_handler(sftp, job):
                    d("[+] Worker [%d] run job [%s] succeed" % (
                        worker_id,
                        job,
                    ))
                else:
                    d("[+] Worker [%d] run job [%s] failed" % (
                        worker_id,
                        job,
                    ))
                    # Add queue, waiting for resubmit
                    job['status'] = False
                    jobs.append(job)
        except Exception as exception:
            e(repr(exception))
            time.sleep(WORKER_WAIT_TIME)


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        jobs.append(create_job(event=event))

    def process_IN_DELETE(self, event):
        jobs.append(create_job(event=event))

    def process_IN_CLOSE_WRITE(self, event):
        jobs.append(create_job(event=event))
        # TODO: put pcap info to polaris
        # jobs.append(create_job(event={
        # }))

    def process_IN_MOVED_TO(self, event):
        jobs.append(create_job(event=event))

    def process_default(self, event):
        # d(event)
        pass


def start_workers():
    for i in range(WORKER_NUMBER):
        t = threading.Thread(target=worker_handler, args=(i, ))
        t.daemon = True
        t.start()


def get_file_list(path):
    return [
        y for x in os.walk(path)
        for y in glob.glob(
            os.path.join(os.path.abspath(x[0]), '*')
        )
    ]


def init_jobs(path):
    files = get_file_list(path)
    for file in files:
        jobs.append(create_job(event={
            "file": file,
            "dir": os.path.isdir(file),
        }))


def main():
    global src
    global dst
    global notifier

    if len(sys.argv) != 4:
        print "Usage : "
        print "\tpython %s [SRC] [DST] [INIT]" % (sys.argv[0])
        exit(0xFF)

    src = os.path.abspath(sys.argv[1])
    dst = sys.argv[2]
    init = (sys.argv[3].lower() == "true")

    if os.path.isfile(src):
        e("Can not monitor on a file")
        return

    # Sync all files first time
    if init:
        init_jobs(src)

    # Start workers
    start_workers()

    # Start pyinotify
    wm = pyinotify.WatchManager()
    wm.add_watch(src, pyinotify.ALL_EVENTS, rec=True)
    eh = EventHandler()
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()


if __name__ == "__main__":
    main()
