#!/usr/bin/env python3
# coding=utf-8
# date 2019-09-11 16:33:51
# author calllivecn <calllivecn@outlook.com>


import os
from os import path
from time import sleep
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

import libevdev as ev
from libevdev import (
                        Device, InputEvent, evbit,
                        EV_REL,EV_KEY,
                        EventsDroppedException,
                        )


import libkbm
from logs import logger


class HotKeyError(Exception):
    pass


class HotKey:
    """
    监听键盘、鼠标事件，触发动作。
    """

    def __init__(self, device=None):
        """
        device: /dev/input/eventX, default: all keyboard.
        """

        self._hotkey_list = []
        self._hotkey_seq_dict = {}

        self.devices = []

        mouses, kbms = libkbm.getkbm() 

        if len(kbms) <= 0:
            raise HotKeyError("没有发现至少一个键盘。")

        if device is None:
            self.kbms = kbms
        else:
            if device not in kbms:
                raise ValueError(f"{device} 不是键盘设备。")
            else:
                self.kbms = device
        
        self.LISTEN = 1
        self.REPLACE = 2
        self._mode = self.LISTEN


        # 把device注册到selectors
        self._selector = DefaultSelector()
        self._fileobjs = []
        for device in self.kbms:
            fd = open(device, "rb")
            devfd = Device(fd)
            self._selector.register(devfd.fd, EVENT_READ, devfd)
            self._fileobjs.append(fd)

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
        
    
    def addhotkey(self, keyseq=(), callback=print):
        """
        keyseq: ["alt", "f"]
        callback: function()
        """
        if not isinstance(keyseq, tuple):
            raise HotKeyError("键序列必须是 tuple !")

        # 预处理
        seq = []
        for key in keyseq:
            key = key.upper()

            if key == "ALT":
                key = "LEFTALT"
            elif key == "CTRL":
                key = "LEFTCTRL"

            key = ev.evbit("KEY_" + key)

            seq.append(key)


        seq_len = len(seq)

        # 判断是否是最后一个键
        last_key = 0
        current_keyseq = self._hotkey_seq_dict
        for key in seq:
            last_key += 1

            if hasattr(current_keyseq, "__call__"):
                raise HotKeyError(f"{seq} 的父键已存在！")

            if key in current_keyseq:

                if last_key < seq_len:
                    current_keyseq = current_keyseq[key]

                elif last_key == seq_len and key in current_keyseq:
                    raise HotKeyError(f"{seq} 按键序列已存在！")

                else:
                    current_keyseq[key] = callback
                    self._hotkey_list.append(seq)


            else:

                if last_key == seq_len:
                    current_keyseq[key] = callback
                    self._hotkey_list.append(seq)
                else:
                    # 一个新的快捷键序列
                    current_keyseq[key] = {}
                    current_keyseq = current_keyseq[key]


    def watch(self):
        """
        return: callback function
        """
        while True:
            for key, event_ in self._selector.select():
                logger.debug("self._selector.select()")

                devfd = key.data
                hotkey = self._hotkey_seq_dict

                try:
                    for e in devfd.events():

                        if e.matches(ev.evbit("EV_KEY")):
                            logger.debug(f"key: {e.code.name} value: {e.value}")
                            logger.debug(f"hotkey: {hotkey}")
                            logger.debug("-"*60)

                            # 这个事件在hotkey seq
                            if e.value == 1 and e.code in hotkey:
                                hotkey = hotkey.get(e.code)
                                if hasattr(hotkey, "__call__"):
                                    return hotkey
                            elif e.value == 0 and e.code in hotkey:
                                hotkey = self._hotkey_seq_dict

                except EventsDroppedException:
                    logger.warning("EventsDroppedException")
                    for e in devfd.sync():
                        logger.debug(e)

        logger.debug("从这里返回的？？？？")

    def watchrun(self):
        func = self.watch()
        func()

    def close(self):
        for fileobj in self._fileobjs:
            if not fileobj.closed:
                fileobj.close()

        self._selector.close()
    
    def __del__(self):
        self.close()





def test():

    logger.setLevel(2)

    hotkey = HotKey()

    hotkey.addhotkey(("alt", "g"), lambda: print("alt+g 成功触发"))

    hotkey.addhotkey(("alt", "f"), lambda: print("alt+f 成功触发"))

    hotkey.addhotkey(("ctrl", "v", "f"), lambda: print("ctrl+v+f 成功触发"))

    logger.debug(hotkey._hotkey_seq_dict)
    while True:
        hotkey.watchrun()


if __name__ == "__main__":
    try:
        test()
    except KeyboardInterrupt:
        pass