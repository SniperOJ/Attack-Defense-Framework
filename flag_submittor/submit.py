#!/usr/bin/env python2

# Acknownledgement: haozigege@Lancet
# Origin repo: https://github.com/zhl2008/flag_service

import logging
import os
import socket
import sys
import signal
import SimpleHTTPServer
import SocketServer
import requests
import cgi
import re
import coloredlogs
import threading 
import time
from time import gmtime, strftime
from urlparse import parse_qs,urlparse
from collections import deque


###### configuration #######

# the listen port
host = "127.0.0.1"
port = 4444

# remote flag submit	
# remote_flag_url = 'https://172.16.4.1/Common/awd_sub_answer'
remote_flag_url = 'http://127.0.0.1:8099/Common/awd_sub_answer.php'

# team token
token = '29b64ae71bb4fd763ad6520c91607a88'

# team cookie
team_cookie = {
    "PHPSESSID":"sa7d5sa67d2gd1y9saa9a"
}

# flag regex pattern
flag_regex_pattern = "[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}"

# flag submit span
time_span = 2

# request time out
time_out = 5

# flag submit log
log_file = './log.cvs'

# load flag from this file
recover_file = './recover'

coloredlogs.install(level='debug')
logging.getLogger("urllib3").setLevel(logging.WARNING)
############################

########## Log functions #########
def l(item, status):
    with open(log_file, "a+") as f:
        if len(f.read()) == 0:
            f.write("status,challenge,victim,attacker,flag,ts\n")

    with open(log_file, "a+") as f:
        data = ",".join([
            status,
            item['challenge'],
            item['victim'],
            item['attacker'],
            item['flag'],
            str(item['ts']),
        ])
        f.write(data + "\n")

def s(item):
    with open(recover_file, "a+") as f:
	data = "%s,%s,%s,%s,%s" % (
            item['challenge'], 
            item['victim'], 
            item['attacker'], 
            item['flag'], 
            str(item['ts']),
        )
        f.write(data + "\n")
############################

########## Recover #########
queue = deque([])
with open(recover_file, "a+") as f:
    '''
    status,challenge,victim,attacker,flag,ts
    '''
    logging.info("Recovering flag from file")
    for line in f:
        data = line.strip().split(",")
        item = {
            "challenge":data[0],
            "victim":data[1],
            "attacker":data[2],
            "flag":data[3],
            "ts":float(data[4]),
        }
        queue.append(item)

logging.info("[%d] items recoverd" % (len(queue)))
with open(recover_file, "w") as f:
    logging.info("Cleaning recover file")
    f.truncate()
############################

########## CTRL+C #########
def sigint_handler(signum, frame):
    for item in queue:
        logging.info("Saveing recover data: %s" % (item))
	s(item)
    exit(0)

signal.signal(signal.SIGINT, sigint_handler)
############################

def search_flag(flag):
    result = re.search(flag_regex_pattern,flag)
    if result == None:
        return ""
    else:
        return result.group()


def flag_submit():
    while True:
        if len(queue) == 0:
            time.sleep(time_span)
            continue
        item = queue.popleft()
        queue.appendleft(item)
        logging.info("[%d] %s" % (len(queue), item))
        flag = item['flag']
        attacker = item['attacker']
        ts = item['ts']

        data = {
            'token':token,
            'answer':flag
        }

        try:
            result = requests.post(
                remote_flag_url,
                cookies=team_cookie,
                data=data,
                timeout=time_out,
                verify=False
            ).content.lower().strip()
            time.sleep(time_span)
            if "retry" in result:
                logging.warning("Retry: %s" % (item))
                l(item, "RETRY")
                continue
            if "right" in result:
                logging.debug("Right flag: %s" % (item))
                queue.popleft()
                l(item, "RIGHT")
                continue
            if "wrong" in result:
                logging.error("Wrong flag: %s" % (item))
                queue.popleft()
                l(item, "WRONG")
                continue
            logging.error("Unknown response: %s" % (result))
        except Exception as e:
            logging.error("Exception: %s" % (str(e)))

class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        '''
        logging.info('"%s" %s %s',self.requestline, str(code), str(size))
        '''
        pass

    def log_message(self, format, *args):
        pass

    def log_error(self, format, *args):
        pass

    def error_handle(self,msg):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(msg)

    def success_handle(self,msg):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(msg)

    def do_GET(self):
        if self.path.startswith('/submit'):
            self.submit_handler()
            return
        if self.path.startswith('/queue'):
            self.success_handle(str(queue))
            return
        if self.path.startswith('/log'):
            self.success_handle(open(log_file).read())
            return
        self.error_handle('404 not found')

    def submit_handler(self):
        params = parse_qs(urlparse(self.path).query)

        params_list = [
                "challenge",
                "victim",
                "attacker",
                "flag",
        ]
        for param in params_list:
            if not params.has_key(param):
                self.error_handle('no %s provided!' % param)
                return

        flag = search_flag(params['flag'][0])

        if flag == "":
            self.error_handle('flag check error!')
            return

        item = {
	    "challenge":params['challenge'][0],
	    "victim":params['victim'][0],
	    "attacker":params['attacker'][0],
	    "flag":flag,
	    "ts":time.time(),
        }

        queue.append(item)

        response = {
            "status":"true",
            "queue":len(queue),
        }
        self.success_handle(str(response))

# update the server_bind function to reuse the port 
class MyTCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

t = threading.Thread(target=flag_submit,name='flag_submit')
t.setDaemon(True)
t.start()

httpd = MyTCPServer((host, port), CustomHTTPRequestHandler)
logging.debug("Server running at %s:%d" % (host, port))
httpd.serve_forever()

