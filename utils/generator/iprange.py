#!/usr/bin/env python
# coding: utf-8
#
# Copyright (C) Michael Ihde 2004 <mike.ihde@randomwalking.com>
#
# Distributed under the Python License
#
# iprange is a useful module that creates iprange generators similar
# to python's xrange.  This allows you to write statements such as
#
# for ip in iprange("192.168.1.0/24")
#     print ip
#
# The above statement will scan the class "C" subnet.  You can also
# use wildcards, or specify a beginning and an end ip address
#
# Revision history
#     0.1       - Aug 17th 2004 : Initial release
#
#
# Todo : Add sanity checks to IP address

import socket
import struct
import re
import sys


class InvalidIPAddress(ValueError):
    """The ip address given to ipaddr is improperly formatted"""


def ipaddr_to_binary(ipaddr):
    """
    A useful routine to convert a ipaddr string into a 32 bit long integer
    """
    # from Greg Jorgensens python mailing list message
    q = ipaddr.split('.')
    return reduce(lambda a, b: long(a) * 256 + long(b), q)


def binary_to_ipaddr(ipbinary):
    """
    Convert a 32-bit long integer into an ipaddr dotted-quad string
    """
    # This one is from Rikard Bosnjakovic
    return socket.inet_ntoa(struct.pack('!I', ipbinary))


def iprange(ipaddr):
    """
    Creates a generator that iterates through all of the IP addresses.
    The range can be specified in multiple formats.

        "192.168.1.0-192.168.1.255"    : beginning-end
        "192.168.1.0/24"               : CIDR
        "192.168.1.*"                  : wildcard
    """
    # Did we get the IP address in the span format?
    span_re = re.compile(r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The beginning IP Address
                             \s*-\s*
                             (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The end IP Address
                          ''', re.VERBOSE)

    res = span_re.match(ipaddr)
    if res:
        beginning = res.group(1)
        end = res.group(2)
        return span_iprange(beginning, end)

    # Did we get the IP address in the CIDR format?
    cidr_re = re.compile(r'''(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # The IP Address
                             /(\d{1,2})                             # The mask
                          ''', re.VERBOSE)

    res = cidr_re.match(ipaddr)
    if res:
        addr = res.group(1)
        cidrmask = res.group(2)
        return cidr_iprange(addr, cidrmask)

    # Did we get the IP address in the wildcard format?
    wild_re = re.compile(r'''(\d{1,3}|\*)\.
                             (\d{1,3}|\*)\.
                             (\d{1,3}|\*)\.
                             (\d{1,3}|\*)   # The IP Address
                          ''', re.VERBOSE)

    res = wild_re.match(ipaddr)
    if res:
        return wildcard_iprange(ipaddr)

    raise InvalidIPAddress


def span_iprange(beginning, end):
    """
    Takes a begining and an end ipaddress and creates a generator
    """
    b = ipaddr_to_binary(beginning)
    e = ipaddr_to_binary(end)

    while (b <= e):
        yield binary_to_ipaddr(b)
        b = b + 1


def cidr_iprange(ipaddr, cidrmask):
    """
    Creates a generator that iterated through all of the IP addresses
    in a range given in CIDR notation
    """
    # Get all the binary one's
    mask = (long(2) ** long(32 - long(cidrmask))) - 1

    b = ipaddr_to_binary(ipaddr)
    e = ipaddr_to_binary(ipaddr)
    b = long(b & ~mask)
    e = long(e | mask)

    while (b <= e):
        yield binary_to_ipaddr(b)
        b = b + 1


def wildcard_iprange(ipaddr):
    """
    Creates a generator that iterates through all of the IP address
    in a range given with wild card notation
    """
    beginning = []
    end = []

    tmp = ipaddr.split('.')
    for i in tmp:
        if i == '*':
            beginning.append("0")
            end.append("255")
        else:
            beginning.append(i)
            end.append(i)

    b = beginning[:]
    e = end[:]

    while int(b[0]) <= int(e[0]):
        while int(b[1]) <= int(e[1]):
            while int(b[2]) <= int(e[2]):
                while int(b[3]) <= int(e[3]):
                    yield b[0] + '.' + b[1] + '.' + b[2] + '.' + b[3]
                    b[3] = "%d" % (int(b[3]) + 1)

                b[2] = "%d" % (int(b[2]) + 1)
                b[3] = beginning[3]

            b[1] = "%d" % (int(b[1]) + 1)
            b[2] = beginning[2]

        b[0] = "%d" % (int(b[0]) + 1)
        b[1] = beginning[1]

def main():
    if len(sys.argv) != 3:
        print "Usage: "
        print "\tpython %s [IP_RANGE] [PORT]" % (sys.argv[0])
        exit(1)

    port = int(sys.argv[2])
    for host in iprange(sys.argv[1]):
        print "%s:%d" % (host, port)

if __name__ == '__main__':
    main()
    '''
    for ip in iprange("192.168.1.1-192.168.1.3"):
        print ip

    for ip in iprange("192.168.1.1/30"):
        print ip

    for ip in iprange("192.168.*.148"):
        print ip

    # Cause an exception
    for ip in iprange("192.168./*.148"):
        phttp://172.rint ip
        '''
