#!/usr/bin/env python

import eventlet

def closed_callback():
    print("called back")

def forward(source, dest, cb=lambda: None):
    while True:
        d = source.recv(32384)
        if d == "":
            cb()
            break
        dest.sendall(d)

listener = eventlet.listen(("localhost", 7000))
while True:
    client, addr = listener.accept()
    server = eventlet.connect(("localhost", 22))
    eventlet.spawn_n(forward, client, server, closed_callback)
    eventlet.spawn_n(forward, server, client)
