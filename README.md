# 使用 libevdev 开发的模拟键盘和鼠标的库

- 使用用时需要root or input 用户组(ubuntu)权限


## 运行开发环境：

```shell
virtualenv Venv
or
python3 -m venv Venv

# 激活虚拟环境
. Venv/bin/activate

pip install .

```

## 运行测试Demo

```shell
mouse.py --help
usage: mouse.py [option] <KeyName>

使用C/S做的，虚拟鼠标键盘。使用前需要先启动server端(用户需要在input用户组内或者使用root启动)。

options:
  -h, --help            输出这个帮助信息
  --list                列出一些可以使用和键的示例
  --secret SECRET       指定通信secret
  --server              启动Server需要input用户组或者root权限。
  --key KEY             按下一个键，后松开。
  --keydown KEYDOWN     按下一个键, 不松开。
  --keyup KEYUP         松开一个键。
  --ctrlkey CTRLKEY     按下ctrl键，加上这个键的组合健。
  --altkey ALTKEY       按下alt键，加上这个键的组合健。
  --shiftkey SHIFTKEY   按下shift键，加上这个键的组合健。
  --mouseclick {left,right,middle}
                        点击鼠标键：必须是：('left', 'right', 'middle') 之一。
  --mousedown {left,right,middle}
                        按下鼠标键：必须是：('left', 'right', 'middle') 之一。
  --mouseup {left,right,middle}
                        释放鼠标键：必须是：('left', 'right', 'middle') 之一。
```

## 查看对应键的键名和键值 运行 input-expoer.py 然后按下键盘上的按键或动下鼠标就可以看到类似如下输出。

```
InputEvent(EV_KEY, KEY_C, 1) # 按下C键时
InputEvent(EV_KEY, KEY_C, 0) # 松开C键时

InputEvent(EV_KEY, KEY_B, 1) # 按下B键时
InputEvent(EV_KEY, KEY_B, 0) # 松开B键时
```

- 在mouse.py --key C
- 在mouse.py --key B
- 在mouse.py --shiftkey B # shift+C


## pyproject.toml 打包方式文档: https://packaging.python.org/en/latest/tutorials/packaging-projects/



## 说明

1. 基础身份信息 (最重要 - 用于识别设备)

- 这些属性帮你确定“这是哪个设备”，尤其是在 /dev/input/eventX 变化时。

  ```text
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
  ```
