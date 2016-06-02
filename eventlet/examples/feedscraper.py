#!/usr/bin/env python

import eventlet
feedparser = eventlet.import_pathched("feedparser")

pool = eventlet.GreenPool()

def fetch_title(url):
    d = feedparser.parse(url)
    return d.feed.get("title", "")

def app(environ, start_response):
    if environ["REQUEST_METHOD"] != "POST":
        start_response("403 Forbidden", [])
        return []

    pile = eventlet.GreenPile(pool)
    for line in environ["wsgi.input"].readlines():
        url = line.strip()
        if url:
            pile.spawn(fetch_title, url)
    titles = "\n".join(pile)
    start_response("200 OK", [("Content-type", "text/plain")])
    return [titles]

if __name__ == "__main__":
    from eventlet import wsgi
    wsgi.server(eventlet.listen(("localhost", 9010)), app)
