#!/usr/bin/env python3
# coding=utf-8
# date 2019-08-13 14:56:48
# author calllivecn <c-all@qq.com>

import os
from os import path

import libevdev
from libevdev import EV_KEY, EV_REL


baseinput="/dev/input"

inputs = []
for fd in os.listdir(baseinput):
    devpath = path.join(baseinput, fd)
    if not path.isdir(devpath):
        inputs.append(open(devpath, 'rb'))

for dev in inputs:
    try:
        device = libevdev.Device(dev)
    except OSError as e :
        #print(dev, "异常.")
        continue

    #if device.has(EV_REL.REL_X) device.has(EV_REL.REL_Y and device.has(EV_KEY.BTN_LEFT) and device.has(EV_KEY.BTN_RIGHT) and device.has(EV_KEY.BTN_MIDDLE) and device.has(EV_KEY.WHEEL):
    MOUSE = [EV_REL.REL_X, EV_REL.REL_Y, EV_REL.REL_WHEEL ,EV_KEY.BTN_LEFT, EV_KEY.BTN_RIGHT, EV_KEY.BTN_MIDDLE]

    KEYBOARD = [EV_KEY.KEY_ESC, EV_KEY.KEY_SPACE, EV_KEY.KEY_BACKSPACE, EV_KEY.KEY_0, EV_KEY.KEY_A, EV_KEY.KEY_Z, EV_KEY.KEY_9, EV_KEY.KEY_F2]

    if all(map(device.has, MOUSE)):
        print("应该是鼠标了: ", device.name, "路径：", device.fd)

    elif all(map(device.has, KEYBOARD)):
        print("应该是键盘了: ", device.name, "路径：", device.fd)

    else:
        print("其他输入设备：", device.name, "路径：",device.fd)

    dev.close()


#with open(path.join(baseinput, "event0"), "rb") as fd:
#    device = libevdev.Device(fd)
#    print(device.name)

