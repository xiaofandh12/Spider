#!/usr/bin/env python

from __future__ import with_statement

from eventlet.green import urllib2
import eventlet
import re

url_regex = re.compile(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))")

def fetch(url, outq):
    print("fetching", url)
    data = ""
    with eventlet.Timeout(5, False):
        data = urllib2.urlopen(url).read()
    for url_match in url_regex.finditer(data):
        new_url = url_match.group(0)
        outq.put(new_url)

def producer(start_url):
    pool = eventlet.GreenPool()
    seen = set()
    q = eventlet.Queue()
    q.put(start_url)
    while True:
        while not q.empty():
            url = q.get()
            if url not in seen and "eventlet.net" in url:
                seen.add(url)
                pool.spawn_n(fetch, url, q)
        pool.waitall()
        if q.empty():
            break
    return seen

seen = producer("http://eventlet.net")
print("I saw these urls:")
print("\n".join(seen))
