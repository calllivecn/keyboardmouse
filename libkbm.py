#!/usr/bin/env python3
# coding=utf-8
# date 2019-09-09 11:43:59
# author calllivecn <c-all@qq.com>


"""
kbm is keyboard mouse
"""

#__all__ = [

import os
import selectors
from os import path
from time import sleep
from threading import Thread


import libevdev as ev
from libevdev import (
                        Device, InputEvent, evbit,
                        EV_REL,EV_KEY
                        )


# from logs import logger, setLevel


def getkbm(baseinput="/dev/input"):
    mouses = []
    keyboards = []
    
    for dev in os.listdir(baseinput):

        devpath = path.join(baseinput, dev)
        if not path.isdir(devpath):
            devfd = open(devpath, 'rb')
        else:
            continue

        try:
            device = Device(devfd)
        except (OSError, Exception) as e :
            logger.info("打开 {} 异常：{}".format(dev, e))
            continue

        if device.name == "Virtual Keyboard Mouse":
            continue
    
        #if device.has(EV_REL.REL_X) device.has(EV_REL.REL_Y and device.has(EV_KEY.BTN_LEFT) and device.has(EV_KEY.BTN_RIGHT) and device.has(EV_KEY.BTN_MIDDLE) and device.has(EV_KEY.WHEEL):
        MOUSE = [EV_REL.REL_X, EV_REL.REL_Y, EV_REL.REL_WHEEL ,EV_KEY.BTN_LEFT, EV_KEY.BTN_RIGHT, EV_KEY.BTN_MIDDLE]
    
        KEYBOARD = [EV_KEY.KEY_ESC, EV_KEY.KEY_SPACE, EV_KEY.KEY_BACKSPACE, EV_KEY.KEY_0, EV_KEY.KEY_A, EV_KEY.KEY_Z, EV_KEY.KEY_9, EV_KEY.KEY_F2]
    
        if all(map(device.has, MOUSE)):
            logger.info("应该是鼠标了: {} 路径：{}".format(device.name, device.fd))
            mouses.append(devpath)
    
        elif all(map(device.has, KEYBOARD)):
            logger.info("应该是键盘了: {} 路径：{}".format(device.name, device.fd))
            keyboards.append(devpath)
    
        #else:
            #print("其他输入设备：", device.name, "路径：",device.fd)
    
        devfd.close()

    return (mouses, keyboards)
    
    #with open(path.join(baseinput, "event0"), "rb") as fd:
    #    device = libevdev.Device(fd)
    #    print(device.name)

def __grab_discard(devicepath):
    """
     devicepath: /dev/input/event17
    """
    logger.debug("disable {}".format(devicepath))

    try:
        fd = open(devicepath, "rb")
        devfd = ev.Device(fd)
    except Exception as e:
        logger.error(f"打开文件描述符 {devicepath} 失败。")
        logger.error(f"异常: {e} ")
        return

    try:
        devfd.grab()
    except ev.device.DeviceGrabError:
        logger.warn("{} grab() 失败".format(devicepath.name))
        return

    for _ in devfd.events():
        pass

def disableDevice(device):
    """
    dev.grab() device.
    """
    with open(device, "rb") as fd:
        if fd.name != "Virtual Keyboard Mouse":
            th = Thread(target=__grab_discard, args=(device,), daemon=True)
            th.start()


class VirtualKeyboardMouse:
    """
    虚拟键盘鼠标
    """
    def __init__(self):
        self.device = Device()
        self.device.name = "Virtual Keyboard Mouse"
        self.__add_mouse_keyboard_events()
        self.uinput = self.device.create_uinput_device()

        # 在创建虚拟输入设备后等一秒，马上使用设备，
        # 会导致事件不生效。
        sleep(1)

        self._delay = 0.01


    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, t):
        if isinstance(t, float) or isinstance(t, int):
            self._delay = t
        else:
            raise ValueError("require is int or float unit seconds.")


    def __add_mouse_keyboard_events(self):
        """
        为虚拟键鼠添加鼠标事件。
        """

        self.device.enable(ev.EV_MSC.MSC_SCAN)

        # 鼠标事件类型
        mouse0 = [ evbit(0, i) for i in range(15) ]
        mouse1 = [ evbit(1, i) for i in range(272, 276+1) ]
        mouse2 = [ evbit(2, 0), evbit(2, 1), evbit(2, 8), evbit(2, 11) ]
        mouse = mouse0 + mouse1 + mouse2

        # 键盘事件类型
        keyboard = [ evbit(1, i) for i in range(1, 128+1) ]

        self.events = mouse + keyboard

        # LEDs
        #led = [ evbit(17, 0), evbit(17, 1), evbit(17, 2) ]

        for e in self.events:
            self.device.enable(e)

    def listkey(self):
        """
        list all support key.
        """
        for e in self.events:
            if e.name.startswith("KEY_"):
                print(e.name.lstrip("KEY_"))
            elif e.name.startswith("BTN_"):
                print(e.name.lstrip("BTN_"))

    def __mousebtn2seq(self, btn, downup=1):
        """
        鼠标点击。
        
        param: btn: LEFT, RIGHT, MIDDLE
        param: downup: 1 or 0
        """
        btn = btn.upper()
        if btn == "LEFT":
            event_seq = [ InputEvent(ev.EV_MSC.MSC_SCAN, value=4),
                            InputEvent(ev.EV_KEY.BTN_LEFT, value=downup),
                            InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]
        elif btn == "RIGHT":
            event_seq = [ InputEvent(ev.EV_MSC.MSC_SCAN, value=4),
                            InputEvent(ev.EV_KEY.BTN_RIGHT, value=downup),
                            InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]
        elif btn == "MIDDLE":
            event_seq = [ InputEvent(ev.EV_MSC.MSC_SCAN, value=4),
                            InputEvent(ev.EV_KEY.BTN_MIDDLE, value=downup),
                            InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]
        else:
            raise ValueError("btn require is LEFT or RIGHT or MIDDLE")

        return event_seq

    def __mousemove2seq(self, rel_x=0, rel_y=0):
        """
        param: (rel_x, rel_y)
        """
        if isinstance(rel_x, int) and isinstance(rel_y, int):
            pass
        else:
            raise ValueError("rel_x rel_y require is int")

        event_seq = [ InputEvent(ev.EV_REL.REL_X, value=rel_x),
                        InputEvent(ev.EV_REL.REL_Y, value=rel_y),
                        InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]

        return event_seq

    def __mousewheel2seq(self, updown=1):
        """
        EV_REL.REL_0B value 与鼠标滚轮方向对应为 -120 or 120
        param: updown: 鼠标滚轮方向，value=1:向上，value=-1 向下
        """
        if updown == 1:
            event_seq = [ InputEvent(ev.EV_REL.REL_WHEEL, value=1),
                            InputEvent(ev.EV_REL.REL_0B, value=120),
                            InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]
        elif updown == -1:
            event_seq = [ InputEvent(ev.EV_REL.REL_WHEEL, value=-1),
                            InputEvent(ev.EV_REL.REL_0B, value=-120),
                            InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]
        else:
            raise ValueError("updown chioce: 1 or -1.")

        return event_seq


    def __key2seq(self, key, downup=1):
        """
        构建事件序列。
        """
        
        if downup == 1 or downup == 0:
            pass
        else:
            raise ValueError("param: downup chioce 1 or 0.")
        

        shiftdown = [ InputEvent(ev.EV_MSC.MSC_SCAN, value=4), 
                    InputEvent(evbit("KEY_LEFTSHIFT"), value=1),
                    InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]

        shiftup = [ InputEvent(ev.EV_MSC.MSC_SCAN, value=4), 
                    InputEvent(evbit("KEY_LEFTSHIFT"), value=0),
                    InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]

        key_seq = [ InputEvent(ev.EV_MSC.MSC_SCAN, value=4), 
                    InputEvent(evbit("KEY_" + key.upper()), value=downup),
                    InputEvent(ev.EV_SYN.SYN_REPORT, value=0) ]

        if key.isupper():
            event_seq = shiftdown + key_seq + shiftup
        elif key.islower():
            event_seq = key_seq
        elif key.isdigit():
            event_seq = key_seq

        return event_seq

    def keydown(self, key):
        """
        按下 key.
        """

        self.uinput.send_events(self.__key2seq(key, 1))
        sleep(self._delay)

    def keyup(self, key):
        """
        松开 key.
        """
        self.uinput.send_events(self.__key2seq(key, 0))
        sleep(self.delay)

    def key(self, key):
        self.keydown(key)
        self.keyup(key)

    def ctrlkey(self, key):
        """
        ctrl+key
        """
        self.keydown("LEFTCTRL")
        self.key(key)
        self.keyup("LEFTCTRL")

    def shiftkey(self, key):
        """
        shift+key
        """
        self.keydown("LEFTSHIFT")
        self.key(key)
        self.keyup("LEFTSHIFT")

    def altkey(self, key):
        """
        alt+key
        """
        self.keydown("LEFTALT")
        self.key(key)
        self.keyup("LEFTALT")

    def mousebtndown(self, btn):
        self.uinput.send_events(self.__mousebtn2seq(btn, downup=1))
        sleep(self._delay)

    def mousebtnup(self, btn):
        self.uinput.send_events(self.__mousebtn2seq(btn, downup=0))
        sleep(self._delay)

    def mouseclick(self, btn):
        # mouse click event list
        self.mousebtndown(btn)
        self.mousebtnup(btn)

    def mousewheel(self, updown):
        """
        updown: "UP" or "DOWN"
        """
        if updown == "UP":
            self.uinput.send_events(self.__mousewheel2seq(1))
        elif updown == "DOWN":
            self.uinput.send_events(self.__mousewheel2seq(-1))
        else:
            raise ValueError("updown: choice UP or DOWN")
        sleep(self._delay)

    def mousemove_relative(self, x, y):
        self.uinput.send_events(self.__mousemove2seq(x, y))
        sleep(self._delay)

    def mousemove(self, x, y):
        """
        还未实现
        """
        #self.uinput.send_events(self.__mousemove2seq(x, y))
        logger.warn("还未实现: mousemove(x, y)")
