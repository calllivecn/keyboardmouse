import libevdev
import os
import glob

class InputDeviceFinder:
    def __init__(self):
        pass

    def find_device_path(self, target_name=None, target_vid=None, target_pid=None):
        """
        遍历 /dev/input/event* 查找匹配的设备。
        
        :param target_name: 设备名称字符串 (支持子字符串匹配)
        :param target_vid: 厂商ID (int), 例如 0x046d
        :param target_pid: 产品ID (int), 例如 0xc077
        :return: 设备的路径 (str) 例如 '/dev/input/event2'，未找到返回 None
        """
        # 获取所有 event 设备
        device_paths = glob.glob("/dev/input/event*")
        
        for path in device_paths:
            fd = -1
            try:
                fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
                device = libevdev.Device(fd)
                
                # 1. 匹配 VID 和 PID (如果提供了)
                if target_vid is not None and target_pid is not None:
                    if device.id.vendor == target_vid and device.id.product == target_pid:
                        return path
                
                # 2. 匹配名称 (如果提供了)
                # 使用 in 判断，防止名字后面带有空格或其他细微差别
                if target_name is not None:
                    if target_name in device.name:
                        return path
                        
            except OSError:
                # 某些设备可能无法打开（权限问题或设备已拔出），跳过
                continue
            finally:
                if fd > -1:
                    os.close(fd)
        
        return None

# ================= 使用示例 =================

if __name__ == "__main__":
    finder = InputDeviceFinder()

    # 方式 A: 通过 VID 和 PID 查找 (最推荐，最准确)
    # 假设 VID=0x046d, PID=0xc077
    found_path = finder.find_device_path(target_vid=0x046d, target_pid=0xc077)
    
    if found_path:
        print(f"✅ 通过 ID 找到设备: {found_path}")
        # 接下来你就可以用这个 path 去做业务逻辑了
        # dev = libevdev.Device(os.open(found_path, os.O_RDONLY))
    else:
        print("❌ 未找到指定的 VID/PID 设备")

    # 方式 B: 通过设备名称查找 (比较直观)
    target_name = "Optical Mouse"
    found_path_by_name = finder.find_device_path(target_name=target_name)
    
    if found_path_by_name:
        print(f"✅ 通过名称找到设备: {found_path_by_name}")
    else:
        print(f"❌ 未找到名称包含 '{target_name}' 的设备")