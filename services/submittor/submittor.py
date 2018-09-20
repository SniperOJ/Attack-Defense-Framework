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
import ConfigParser
from time import gmtime, strftime
from urlparse import parse_qs,urlparse
from collections import deque


###### configuration #######
config = ConfigParser.ConfigParser()
config.read('./config.ini')  

# the listen port
host = "127.0.0.1"
port = 4444

# remote flag submit	
remote_flag_url = 'http://127.0.0.1:50000/flag.php'

# team token
token = '443ee509c8f1c0ea'

# team cookie
cookies = {
    "PHPSESSID":""
}

# flag regex pattern
# flag_regex_pattern = "[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}"
flag_regex_pattern = "flag\{[0-9a-fA-F]{32}\}"
# flag_regex_pattern = "[0-9a-fA-F]{64}"
# flag_regex_pattern = "flag\{[0-9a-fA-F]{32}\}"

# flag submit span
time_span = 0.5

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
            f.write("id,status,challenge,victim,attacker,flag,ts\n")

    with open(log_file, "a+") as f:
        data = ",".join([
            str(item['id']),
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
	data = "%d,%s,%s,%s,%s,%s" % (
            str(item['id']),
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
    id,status,challenge,victim,attacker,flag,ts
    '''
    logging.info("Recovering flag from file")
    for line in f:
        data = line.strip().split(",")
        item = {
            "id":int(data[0]),
            "challenge":data[1],
            "victim":data[2],
            "attacker":data[3],
            "flag":data[4],
            "ts":float(data[5]),
        }
        queue.append(item)

logging.info("[%d] items recoverd" % (len(queue)))
with open(recover_file, "w") as f:
    logging.info("Cleaning recover file")
    f.truncate()
############################

########## CTRL+C #########
def sigint_handle(signum, frame):
    for item in queue:
        logging.info("Saveing recover data: %s" % (item))
	s(item)
    exit(0)

signal.signal(signal.SIGINT, sigint_handle)
############################

def search_flag(flag):
    result = re.search(flag_regex_pattern,flag)
    if result == None:
        return ""
    else:
        return result.group()

def update_log_status(log_id, status):
    url = "http://%s:%d/api/%s/%d/" % (
        config.get("sirius", "host"), 
        int(config.get("sirius", "port")), 
        "log",
        int(log_id),
    )
    print url
    data = {
        "status":status,
    }
    response = requests.patch(url, headers={
        'Authorization': 'Bearer %s' % (config.get("sirius", "token")), 
    }, data=data)
    print response.content


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
        log_id = int(item['id'])
        print item

        # Update Log status to pending
        update_log_status(log_id, "PENDING")

        params = {
            'token':token,
            'flag':flag
        }

        try:
            result = requests.post(
                remote_flag_url,
                params=params,
                timeout=time_out,
                cookies=cookies,
                verify=False,
            ).content.lower().strip()
            print "Response: %s" %  result
            time.sleep(time_span)
            if "retry" in result:
                logging.warning("Retry: %s" % (item))
                l(item, "RETRY")
                update_log_status(log_id, "FRESH")
                continue
            if "right" in result:
                logging.debug("right flag: %s" % (item))
                queue.popleft()
                l(item, "right")
                update_log_status(log_id, "RIGHT")
                continue
            if "wrong" in result:
                logging.error("wrong flag: %s" % (item))
                queue.popleft()
                l(item, "WRONG")
                update_log_status(log_id, "WRONG")
                continue
            logging.error("Unknown response: %s" % (result))
        except Exception as e:
            logging.error("Exception: %s" % (str(e)))

class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        pass

    def log_message(self, format, *args):
        pass

    def log_error(self, format, *args):
        pass

    def success_handle(self,msg):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(msg)

    def error_handle(self,msg):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(msg)

    def do_GET(self):
        self.submit_handle()

    def submit_handle(self):
        params = parse_qs(urlparse(self.path).query)
        params_list = [
                "challenge",
                "victim",
                "attacker",
                "flag",
                "id",
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
            "id":params['id'][0]
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
