from appium import webdriver
from typing import Dict, Any
from config import load_config

class AppiumDriver:
    """Appium驱动管理类（单例模式）"""
    _instance = None  # 单例实例
    
    @classmethod
    def get_driver(cls, platform: str = "ios") -> webdriver.Remote:
        """获取Appium驱动实例
        Args:
            platform: 平台类型（ios/android）
        """
        if not cls._instance:
            config = load_config()
            # 获取设备能力配置
            capabilities = config['devices'][platform]
            # 设置自动化引擎
            capabilities['automationName'] = 'XCUITest' if platform == 'ios' else 'UiAutomator2'
            # 获取设备UDID
            capabilities['udid'] = cls._get_device_udid(platform)
            
            # 构造Appium服务地址
            server_url = f"http://{config['appium_server']['host']}:{config['appium_server']['port']}/wd/hub"
            # 创建驱动实例
            cls._instance = webdriver.Remote(server_url, capabilities)
        return cls._instance
    
    @classmethod
    def quit_driver(cls):
        """退出并重置驱动实例"""
        if cls._instance:
            cls._instance.quit()
            cls._instance = None
            
    def _get_device_udid(self, platform: str) -> str:
        """获取设备UDID（iOS专用）
        Args:
            platform: 平台类型
        """
        device_manager = DeviceManager()
        devices = device_manager.get_ios_devices() if platform == 'ios' else []
        return devices[0].udid if devices else ""  # 返回第一个设备的UDID 