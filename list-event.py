"""
1. 基础身份信息 (最重要 - 用于识别设备)
这些属性帮你确定“这是哪个设备”，尤其是在 /dev/input/eventX 变化时。
name (str):
设备的名称。
示例: "Logitech USB Optical Mouse"
id (object):
包含设备的 ID 信息。它有四个子属性：
vendor: 厂商ID (VID)，如 0x046d。
product: 产品ID (PID)，如 0xc077。
bustype: 总线类型（USB, Bluetooth等）。
version: 版本号。
用途: 这是最靠谱的区分设备的方法。
phys (str):
物理路径。显示设备插在哪个物理端口上。
示例: "usb-0000:00:14.0-1/input0"
用途: 如果你有两个一模一样的鼠标（VID/PID 相同），可以通过这个区分。只要不换 USB 口，这个字符串就不变。
uniq (str):
唯一标识符（通常是序列号）。
注意: 很多便宜的 USB 设备这个字段是空的。如果是蓝牙设备，通常是 MAC 地址。
devnode (str):
当前关联的设备节点路径。
示例: "/dev/input/event3"
syspath (str):
在 /sys 文件系统中的路径。
driver_version (int):
底层 evdev 驱动的版本。
"""

import os
# import traceback
from pathlib import Path
import libevdev

baseinput="/dev/input"

inputs = []
for devnode in os.listdir(baseinput):
    devpath = Path(baseinput) / devnode
    if not devpath.is_dir():
        inputs.append(devpath)


def list_all_devices():
    print(f"{'Path':<20} {'Bus':<6} {'VID':<6} {'PID':<6} {'Name'}")
    print("-" * 60)

    # 遍历所有可能的 event 节点
    for path in inputs:
        with open(path, "rb") as fp:
            try:
                # 以只读方式打开设备
                device = libevdev.Device(fp)

                # 获取设备信息
                name = device.name
                vid = device.id["vendor"]
                pid = device.id["product"]
                bus = device.id["bustype"]

                # 打印信息 (VID/PID 格式化为 16 进制)
                print(f"{path} {bus=} {vid=:04x} {pid=:04x} {name=} {device=} {device.id=} {device.phys}")
                # print(f"{path} {bus=} {vid=:04x} {pid=:04x} {name=} {device=} {device.id=} {dir(device)=}")

            except OSError as e:
                print(f"{path=} [Error: {e}]")
                # traceback.print_exception(e)
            except Exception as e:
                print(f"{path=} [Error: {e}]")
                # traceback.print_exception(e)


if __name__ == "__main__":
    list_all_devices()