#!/usr/bin/env python

import eventlet
from eventlet.green import urllib2

urls = [
    "http://www.baidu.com/",
    "http://www.douban.com/"
]

def fetch(url):
    print("opening", url)
    body = urllib2.urlopen(url).read()
    print("done with", url)
    return url, body

pool = eventlet.GreenPool(200)
for url, body in pool.imap(fetch, urls):
    print("got body from", url, "of length", len(body))
