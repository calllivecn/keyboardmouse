#!/usr/bin/env python3
# coding=utf-8
# date 2021-08-31 21:33:15
# author calllivecn <calllivecn@outlook.com>

import sys
import socket
import struct
import argparse
import traceback
from enum import Enum, auto

from keyboardmouse.libkbm import VirtualKeyboardMouse

# lenght 32 byte
SECRET=b"0bV2mzu1mDVnfVJus2g0RcJ3wW6qYXLg"

ADDR=("::1", 15886)

MouseKeys=("left", "right", "wheel")

class KeySeq(Enum):
    Key = auto()
    KeyDown = auto()
    KeyUp = auto()
    CtrlKey = auto()
    AltKey = auto()
    ShiftKey = auto()

    MouseClick = auto()
    MouseDown = auto()
    MouseUp = auto()

class SecretError(Exception):
    pass

class ProtocolVersionError(Exception):
    pass

class MouseError(Exception):
    pass

# 拿到可用的keyname
KeyNames = VirtualKeyboardMouse().keyevents2strings

class Cmd:

    def __init__(self, secret):
        """
        pack 格式：
        32byte scret,
        1byte version,
        2byte Key 序号,
        键名 字符串， 不定长度, 为剩下的内容。
        """

        self.secret = secret

        self.cmdformat = struct.Struct("!32sBH")
        self.version = 0x01

    def tobyte(self, KeyName, keyseq):
        binaray = self.cmdformat.pack(self.secret, self.version, keyseq.value)
        return binaray + KeyName.encode("ascii")
    
    def frombyte(self, buf):
        tmp = self.cmdformat.unpack(buf[:self.cmdformat.size])
        keyname = buf[self.cmdformat.size:].decode("ascii")
        secret, version, keyseq = tmp

        keyseq = KeySeq(keyseq)

        print("debug: ", tmp, keyseq, keyname)

        if secret != self.secret:
            raise SecretError("The secret is wrong, please check the secret.")
        
        if version != self.version:
            raise ProtocolVersionError("Wrong protocol version")
    
        if keyseq not in KeySeq: # or keyname not in KeyNames:
            raise MouseError("KeySeq error or") # keyname error")

        self.keyseq = keyseq
        self.keyname = keyname


def inputkey(mouse, cmd):
    # 
    if cmd.keyseq == KeySeq.MouseClick:
        mouse.mouseclick(cmd.keyname)

    elif cmd.keyseq == KeySeq.MouseDown:
        mouse.mousebtndown(cmd.keyname)

    elif cmd.keyseq == KeySeq.MouseUp:
        mouse.mousebtnup(cmd.keyname)

    elif cmd.keyseq == KeySeq.Key:
        mouse.key(cmd.keyname)

    elif cmd.keyseq == KeySeq.KeyDown:
        mouse.keydown(cmd.keyname)

    elif cmd.keyseq == KeySeq.KeyUp:
        mouse.keyup(cmd.keyname)

    elif cmd.keyseq == KeySeq.CtrlKey:
        mouse.ctrlkey(cmd.keyname)

    elif cmd.keyseq == KeySeq.AltKey:
        mouse.altkey(cmd.keyname)

    elif cmd.keyseq == KeySeq.ShiftKey:
        mouse.shiftkey(cmd.keyname)



def server(secret):
    mouse = VirtualKeyboardMouse()
    mouse.create_device()

    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    sock.bind(ADDR)

    while True:
        data, addr = sock.recvfrom(64)
        cmd = Cmd(secret)
        try:
            cmd.frombyte(data)
        except Exception as e:
            print(e)
            sock.sendto(e.args[0].encode("utf8"), addr)
            continue
        
        try:
            inputkey(mouse, cmd)
        except AssertionError as e:
            traceback.print_exc()
            print("Error Key:", cmd.keyname)
            sock.sendto(b"Error", addr)
            continue

        sock.sendto(b"ok", addr)


def client(cmd, keyseq, keyname):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    sock.settimeout(3)

    data = cmd.tobyte(keyname, keyseq)

    sock.sendto(data, ADDR)

    try:
        data, addr = sock.recvfrom(64)
    except socket.timeout:
        print("收到确认超时")
        sys.exit(2)

    if data == b"ok":
        # print("ok")
        sys.exit(0)
    else:
        print("error: ", data)

    sock.close()


def check_secret(s):
    if len(s) != 32:
        raise argparse.ArgumentTypeError("secret 必须是32位可打印 ASCII字符")
    
    try:
        s_byte = s.encode("ascii")
    except Exception:
        raise argparse.ArgumentTypeError("secret 必须是32位可打印 ASCII字符")
    
    return s_byte


def main():

    parse = argparse.ArgumentParser(
        usage="%(prog)s [option] <KeyName>",
        description="使用C/S做的，虚拟鼠标键盘。"
        "使用前需要先启动server端(用户需要在input用户组内或者使用root启动)。",
        add_help=False,
        epilog="",
    )

    parse.add_argument("-h", "--help", action="store_true", help="输出这个帮助信息")
    parse.add_argument("--list", action="store_true", help="列出一些可以使用和键的示例")
    parse.add_argument("--secret", action="store", default=SECRET, type=check_secret, help="指定通信secret")

    group = parse.add_mutually_exclusive_group()
    group.add_argument("--server", action="store_true", help="启动Server需要input用户组或者root权限。")

    group.add_argument("--key", action="store", help="按下一个键，后松开。")
    group.add_argument("--keydown", action="store", help="按下一个键, 不松开。")
    group.add_argument("--keyup", action="store", help="松开一个键。")
    group.add_argument("--ctrlkey", action="store", help="按下ctrl键，加上这个键的组合健。")
    group.add_argument("--altkey", action="store", help="按下alt键，加上这个键的组合健。")
    group.add_argument("--shiftkey", action="store", help="按下shift键，加上这个键的组合健。")
    group.add_argument("--mouseclick", action="store", choices=MouseKeys, help=f"点击鼠标键：必须是：{MouseKeys} 之一。")
    group.add_argument("--mousedown", action="store", choices=MouseKeys, help=f"按下鼠标键：必须是：{MouseKeys} 之一。")
    group.add_argument("--mouseup", action="store", choices=MouseKeys, help=f"释放鼠标键：必须是：{MouseKeys} 之一。")

    args = parse.parse_args()

    if args.help:
        parse.print_help()
        sys.exit(0)
    
    if args.list:
        for kn in KeyNames:
            print(kn)

        sys.exit(0)
    
    if args.server:
        try:
            server(args.secret)
        except KeyboardInterrupt:
            pass

        sys.exit(0)
    
    cmd = Cmd(args.secret)
    if args.key:
        client(cmd, KeySeq.Key, args.key)
    elif args.keydown:
        client(cmd, KeySeq.KeyDown, args.keydown)
    elif args.keyup:
        client(cmd, KeySeq.KeyUp, args.keyup)
    elif args.ctrlkey:
        client(cmd, KeySeq.CtrlKey, args.ctrlkey)
    elif args.altkey:
        client(cmd, KeySeq.AltKey, args.altkey)
    elif args.shiftkey:
        client(cmd, KeySeq.ShiftKey, args.shiftkey)
    elif args.mouseclick:
        client(cmd, KeySeq.MouseClick, args.mouseclick)
    elif args.mousedown:
        client(cmd, KeySeq.MouseDown, args.mousedown)
    elif args.mouseup:
        client(cmd, KeySeq.MouseUp, args.mouseup)
    else:
        parse.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
