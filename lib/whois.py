#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2010  Carlos Perez
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; Applies version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import re
from netaddr import *

def get_whois(ip_addrs):
    """
    Function that returns what whois server is the one to be queried for
    registration information, returns whois.arin.net is not in database, returns
    None if private.
    """
    whois_server = None
    ip = IPAddress(ip_addrs)
    info_of_ip = ip.info
    if ip.version == 4 and ip.is_private() == False:
        for i in info_of_ip['IPv4']:
            whois_server = i['whois']
            if len(whois_server) == 0 and i['status'] != "Reserved":
                whois_server = "whois.arin.net"
            elif len(whois_server) == 0:
                whois_server = None

    return whois_server


def whois(target,whois_srv):
    """
    Performs a whois query against a arin.net for a given IP, Domain or Host as a
    string and returns the answer of the query.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((whois_srv, 43))
    s.send(target + "\r\n")
    response = ''
    while True:
        d = s.recv(4096)
        response += d
        if d == '':
            break
    s.close()
    return response


def get_whois_nets(data):
    """
    Parses whois data and extracts the Network Ranges returning an array of lists
    where each list has the starting and ending IP of the found range.
    """
    patern = '([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
    results = re.findall(patern,data)
    return results