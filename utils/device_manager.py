import tidevice
import subprocess
from typing import Dict, Any, List

class DeviceManager:
    """设备管理类，用于处理iOS设备连接和WDA服务"""
    
    def __init__(self):
        # tidevice不需要实例化
        pass
        
    def get_ios_devices(self) -> list:
        """获取所有连接的iOS设备列表"""
        try:
            devices = tidevice.Usbmux().device_list()
            return [d.udid for d in devices] if devices else ["未检测到设备"]
        except Exception:
            return ["未检测到设备"]
    
    def get_device_info(self, udid: str) -> Dict[str, Any]:
        """获取指定设备的详细信息
        Args:
            udid: 设备唯一标识
        Returns:
            包含设备信息的字典
        """
        try:
            device = tidevice.Device(udid)
            return {
                "udid": udid,
                "name": device.name,  # 设备名称
                "model": device.model,  # 设备型号
                "version": device.product_version  # 系统版本
            }
        except Exception:
            return {
                "udid": udid,
                "name": "Unknown",
                "model": "Unknown",
                "version": "Unknown"
            }
    
    def start_wda(self, udid: str, port: int = 8100):
        """启动WebDriverAgent服务
        Args:
            udid: 设备唯一标识
            port: 服务端口号
        Returns:
            WebDriverAgent服务实例
        """
        device = tidevice.Device(udid)
        service = tidevice.Service(device)
        service.start_wda(port=port)  # 启动WDA服务
        return service

    def get_all_devices(self) -> Dict[str, List[Dict]]:
        """获取所有已连接设备"""
        return {
            "iOS": self.get_ios_devices_info(),
            "Android": self.get_android_devices_info()
        }

    def get_ios_devices_info(self) -> List[Dict]:
        """获取iOS设备详细信息"""
        devices = []
        try:
            for device in tidevice.Usbmux().device_list():
                try:
                    dev = tidevice.Device(device.udid)
                    devices.append({
                        "udid": device.udid,
                        "name": dev.name,
                        "model": dev.model,
                        "version": dev.product_version,
                        "status": "connected"
                    })
                except Exception:
                    continue
        except Exception:
            pass
            
        return devices if devices else [{"udid": "未检测到设备", "name": "N/A", "model": "N/A", "version": "N/A", "status": "disconnected"}]

    def get_android_devices_info(self) -> List[Dict]:
        """获取Android设备信息"""
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        devices = []
        for line in result.stdout.split('\n')[1:]:
            if '\tdevice' in line:
                udid = line.split('\t')[0]
                devices.append({
                    "udid": udid,
                    "name": self._get_android_device_name(udid),
                    "model": self._get_android_prop(udid, 'ro.product.model'),
                    "version": self._get_android_prop(udid, 'ro.build.version.release'),
                    "status": "connected"
                })
        return devices if devices else [{"udid": "未检测到设备", "name": "N/A", "model": "N/A", "version": "N/A", "status": "disconnected"}]

    def _get_android_device_name(self, udid: str) -> str:
        """获取Android设备名称"""
        return self._get_android_prop(udid, 'ro.product.name')

    def _get_android_prop(self, udid: str, prop: str) -> str:
        """获取Android设备属性"""
        result = subprocess.run(
            ['adb', '-s', udid, 'shell', 'getprop', prop],
            capture_output=True, text=True
        )
        return result.stdout.strip() or "N/A" 