#!/usr/bin/env python3
# coding=utf-8
# date 2021-08-31 21:33:15
# author calllivecn <c-all@qq.com>

import sys
import socket

from libkbm import VirtualKeyboardMouse

SECRET=b"llibsslfjea e;ilie"

ADDR=("127.0.0.1", 15886)

def server():
    mouse = VirtualKeyboardMouse()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(ADDR)

    while True:

        data, addr = sock.recvfrom(64)
        if data == SECRET:
            mouse.mouseclick("right")

        sock.sendto(b"ok", addr)



def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(SECRET, ADDR)
    data, addr = sock.recvfrom(64)

    if data == b"ok":
        print("ok")
    else:
        print("error")

    sock.close()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        client()
    elif len(sys.argv) == 2 and sys.argv[1] == "server":
        server()
    else:
        print(f"Usage: {sys.argv[0]}")
        print(f"Usage: {sys.argv[0]} server")
        sys.exit(1)
