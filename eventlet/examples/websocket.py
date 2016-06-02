#!/usr/bin/env python

import eventlet
from eventlet import wsgi
from eventlet import websocket
from eventlet.support import six

import os
import random

@websocket.WebSocketWSGI
def handle(ws):
    if ws.path == "/echo":
        while True:
            m = ws.wait()
            if m is None:
                break
            ws.send(m)
    elif ws.path == "/data":
        for i in six.moves.range(1000):
            ws.send("0 %s %s\n" % (i, random.random()))
            eventlet.sleep(0.1)

def dispatch(environ, start_response):
    if environ["PATH_INFO"] == "/data":
        return handle(environ, start_response)
    else:
        start_response("200 OK", [("content-type", "text/html")])
        return [open(os.path.join(os.path.dirname(__file__),"websocket.html")).read()]

if __name__ == "__main__":
    listener = eventlet.listen(("127.0.0.1", 7000))
    print("\nVisit http://localhost:7000/ in your websocket-capable browser.\n")
    wsgi.server(listener, dispatch)
