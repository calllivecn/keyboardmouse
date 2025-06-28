#!/usr/bin/env python3
# coding=utf-8
# date 2019-08-13 18:12:34
# author calllivecn <calllivecn@outlook.com>


import os
import sys
import selectors
#import fcntl

import libevdev as ev
from libevdev import Device, InputEvent

from keyboardmouse import libkbm


def registers(kbms, selector):

    for kbm in kbms:
        print("加入：", kbm)
        fd = os.open(kbm, os.O_NONBLOCK | os.O_RDONLY)
        fdobj = open(fd, "rb")
        #fcntl.fcntl(fd, fcntl.F_SETFL, os.O_NONBLOCK)
        device = Device(fdobj)

        selector.register(device.fd, selectors.EVENT_READ, data=device)



def run(s):
    mouses, keyboards = libkbm.getkbm()
    registers(mouses + keyboards, s)

    while True:
        #print("while 里面")
        for fd, event in s.select():
            #print("for select() 里面")
            try:
                for e in fd.data.events():
                    #print("for events() 里面")
                    if e.matches(ev.EV_KEY):
                        print(e)
                    else:
                        print("======= 不是key事件：=======", e)
            except ev.EventsDroppedException:
                print("eventsDroppedException:")
                for err in ev.sync():
                    print("except:", err)



with selectors.DefaultSelector() as s:
    run(s)

"""
成功了～～～
"""

