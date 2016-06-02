#!/usr/bin/env python

from __future__ import with_statement

from eventlet.green import urllib2
import eventlet
import re

url_regex = re.compile(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))")

def fetch(url, seen, pool):
    print("fetching", url)
    data = ""
    with eventlet.Timeout(5, False):
        data = urllib2.urlopen(url).read()
    for url_match in url_regex.finditer(data):
        new_url = url_match.group(0)
        if new_url not in seen and "eventlet.net" in new_url:
            seen.add(new_url)
            pool.spawn_n(fetch, new_url, seen, pool)

def crawl(start_url):
    pool = eventlet.GreenPool()
    seen = set()
    fetch(start_url, seen, pool)
    pool.waitall()
    return seen

seen = crawl("http://eventlet.net")
print("I saw these urls:")
print("\n".join(seen))
