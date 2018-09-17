#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tcp Port Forwarding (Reverse Proxy)
# Author : WangYihang <wangyihanger@gmail.com>


import socket
import threading
import sys


def handle(buffer):
    return buffer


def transfer(src, dst, direction):
    src_name = src.getsockname()
    src_address = src_name[0]
    src_port = src_name[1]
    dst_name = dst.getsockname()
    dst_address = dst_name[0]
    dst_port = dst_name[1]
    while True:
        buffer = src.recv(0x400)
        if len(buffer) == 0:
            print "[-] No data received! Breaking..."
            break
        # print "[+] %s:%d => %s:%d [%s]" % (src_address, src_port, dst_address, dst_port, repr(buffer))
        if direction:
            print "[+] %s:%d >>> %s:%d [%d]" % (src_address, src_port, dst_address, dst_port, len(buffer))
        else:
            print "[+] %s:%d <<< %s:%d [%d]" % (dst_address, dst_port, src_address, src_port, len(buffer))
        dst.send(handle(buffer))
    print "[+] Closing connecions! [%s:%d]" % (src_address, src_port)
    src.shutdown(socket.SHUT_RDWR)
    src.close()
    print "[+] Closing connecions! [%s:%d]" % (dst_address, dst_port)
    dst.shutdown(socket.SHUT_RDWR)
    dst.close()


def server(local_host, local_port, remote_host, remote_port, max_connection):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(max_connection)
    print '[+] Server started [%s:%d]' % (local_host, local_port)
    print '[+] Connect to [%s:%d] to get the content of [%s:%d]' % (local_host, local_port, remote_host, remote_port)
    while True:
        local_socket, local_address = server_socket.accept()
        print '[+] Detect connection from [%s:%s]' % (local_address[0], local_address[1])
        print "[+] Trying to connect the REMOTE server [%s:%d]" % (remote_host, remote_port)
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        print "[+] Tunnel connected! Tranfering data..."
        # threads = []
        s = threading.Thread(target=transfer, args=(
            remote_socket, local_socket, False))
        r = threading.Thread(target=transfer, args=(
            local_socket, remote_socket, True))
        # threads.append(s)
        # threads.append(r)
        s.start()
        r.start()
    print "[+] Releasing resources..."
    remote_socket.shutdown(socket.SHUT_RDWR)
    remote_socket.close()
    local_socket.shutdown(socket.SHUT_RDWR)
    local_socket.close()
    print "[+] Closing server..."
    server_socket.shutdown(socket.SHUT_RDWR)
    server_socket.close()
    print "[+] Server shuted down!"


def main():
    if len(sys.argv) != 5:
        print "Usage : "
        print "\tpython %s [L_HOST] [L_PORT] [R_HOST] [R_PORT]" % (sys.argv[0])
        print "Example : "
        print "\tpython %s 127.0.0.1 8888 127.0.0.1 22" % (sys.argv[0])
        print "Author : "
        print "\tWangYihang <wangyihanger@gmail.com>"
        exit(1)
    LOCAL_HOST = sys.argv[1]
    LOCAL_PORT = int(sys.argv[2])
    REMOTE_HOST = sys.argv[3]
    REMOTE_PORT = int(sys.argv[4])
    MAX_CONNECTION = 0x10
    server(LOCAL_HOST, LOCAL_PORT, REMOTE_HOST, REMOTE_PORT, MAX_CONNECTION)


if __name__ == "__main__":
    main()
