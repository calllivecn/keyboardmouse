
# 这是直接使用命令行
# systemd-inhibit --what=idle --who="uinput-bot" --why="Keep Mutter frame clock active for Wayland game" python3 your_script.py

import asyncio
from dbus_next.aio import MessageBus

async def take_idle_inhibit_lock():
    bus = await MessageBus(system=True).connect()
    introspection = await bus.introspect('org.freedesktop.login1', '/org/freedesktop/login1')
    obj = bus.get_proxy_object('org.freedesktop.login1', '/org/freedesktop/login1', introspection)
    manager = obj.get_interface('org.freedesktop.login1.Manager')
    
    # 申请 idle 锁，返回一个 open file descriptor
    fd = await manager.call_inhibit('idle', 'uinput-script', 'Disable Mutter Throttling', 'block')
    print("Inhibit lock acquired, FD:", fd)
    return fd # 保持 fd 打开，不要被垃圾回收；进程退出时内核会自动关闭 FD 并释放锁

# 运行你的 uinput 模拟逻辑...



