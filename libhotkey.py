#!/usr/bin/env python3
# coding=utf-8
# date 2019-09-11 16:33:51
# author calllivecn <c-all@qq.com>


import os
from os import path
from time import sleep


import libevdev as ev
from libevdev import (
                        Device, InputEvent, evbit,
                        EV_REL,EV_KEY
                        )


import libkbm
from logs import logger

class HotKey:
    """
    监听键盘、鼠标事件，触发动作。
    """

    def __init__(self, device=None):
        """
        device: /dev/input/eventX, default: all keyboard and mouse.
        """

        self.devices = []

        kbms = getkbm() 

        if len(kbms) <= 0:
            raise Exception("没有发现至少一个键盘或鼠标。")

        if device is None:
            self.kbms = kbms
        else:
            if device not in kbms:
                raise ValueError("{} 不是鼠标或键盘设备。".format(device))
            else:
                self.kbms = device
        
        self.LISTEN = 1
        self.REPLACE = 2
        self._mode = self.LISTEN

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, m):
        """
        m: replace mode: self.REPLACE, listen mode: self.LISTEN (default)
        """
        if m == self.REPLACE or m == self.LISTEN:
            self._mode = m
        else:
            raise ValueError("mode is choice: self.REPLACE or self.LISTEN")
        
    
    def addhotkey(self, hotkeys=[], callback=print):
        """
        hotkeys: ["alt", "f"]
        callback: function()
        """


    def monitor(self):
        pass


