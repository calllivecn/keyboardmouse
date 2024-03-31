#!/usr/bin/env python3
# coding=utf-8
# date 2019-08-13 18:12:34
# author calllivecn <calllivecn@outlook.com>


import os
import sys
import time
import selectors
#import fcntl

import libevdev as ev
from libevdev import Device, InputEvent

from keyboardmouse import libkbm

REPLACE = 1 
LISTEN = 2
MODE = LISTEN

"""
replace 模式，还有问题: 放滞...
    Device(fd) 设备，不能直接device.send_events()写回。
"""


def registers(kbms):
    print(f"{kbms=}")
    selector = selectors.DefaultSelector()

    for kbm in kbms:
        print("加入：", kbm)
        fd = os.open(kbm, os.O_NONBLOCK | os.O_RDONLY)
        #fd = os.open(kbm, os.O_NONBLOCK | os.O_RDWR)
        fdobj = open(fd, "rb")
        device = Device(fdobj)

        if MODE == REPLACE:
            #uinput.grab()
            pass
        elif MODE == LISTEN:
            pass

        selector.register(device.fd, selectors.EVENT_READ, data=device)

    return selector


key_prefix = ( ev.InputEvent(ev.EV_KEY.KEY_LEFTALT), ev.InputEvent(ev.EV_KEY.KEY_RIGHTALT) )
key_prefix_flag = False
hotkeys = ["f"]

def addhotkey(keys=[], callback=print):
    pass
    

def listenhotkey(e):
    """
    replace 模式：
        把一个指定序列，替换成别一个hotkye序列。
        如果不是指定序列，原样写回设备。
        有序列保存，写回问题。
    listen 模式：
       监听到指定序列后，增加一个hotkey序列。

    难点：
       如何正确匹配hotkey序列，如果不匹配如何写回设备，不影响原序列。
    """
    
    global key_prefix_flag

    if key_prefix_flag == True:
        if e.matches(ev.EV_KEY.KEY_F, value=1):
            print("ALT+F 快捷键 匹配成功。")

    if e.matches(ev.EV_KEY.KEY_LEFTALT, value=1):
        print(time.asctime(), "matches LEFTALT down")
        key_prefix_flag = True

    elif e.matches(ev.EV_KEY.KEY_LEFTALT, value=0):
        print(time.asctime(), "matches LEFTALT up")
        key_prefix_flag = False

    else:
        return False

    return True


mouses, keyboards = libkbm.getkbm()
s = registers(keyboards)

while True:
    for fd, _ in s.select():
        try:
            events = fd.data.events()
        except ev.EventsDroppedException:
            print("eventsDroppedException:")
            for err in ev.sync():
                print("except:", err)
            continue

        for e in events:
            if e.matches(ev.EV_KEY):
                if listenhotkey(e):
                    pass
                else:
                    print(time.asctime(), e)
            else:
                #print("======= 不是key事件：=======", e)
                pass


