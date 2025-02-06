from appium.webdriver.common.mobileby import MobileBy
from typing import Tuple

class LocatorParser:
    @staticmethod
    def parse(locator_config: dict, platform: str) -> tuple:
        """
        解析定位配置为Appium定位器
        :param locator_config: 定位配置字典（包含ios/android键）
        :param platform: 当前平台（ios/android）
        :return: (定位方式, 定位表达式) 元组
        """
        # 新增策略判断
        if 'accessibility_id' in locator_config:
            return (MobileBy.ACCESSIBILITY_ID, locator_config['accessibility_id'])
        
        # 处理带策略标识的定位器
        if locator_config.get('strategy'):
            strategy = locator_config['strategy']
            value = locator_config['value']
            return (strategy, value)
        
        # 修改原有平台判断逻辑
        if platform == 'ios':
            if locator_config['ios'].startswith('//'):  # XPath
                return (MobileBy.XPATH, locator_config['ios'])
            elif locator_config['ios'].startswith('class='):
                return (MobileBy.CLASS_NAME, locator_config['ios'].split('=')[1])
            else:  # Predicate
                return (MobileBy.IOS_PREDICATE, locator_config['ios'])
        else:
            if locator_config['android'].startswith('//'):  # XPath
                return (MobileBy.XPATH, locator_config['android'])
            else:  # UIAutomator
                return (MobileBy.ANDROID_UIAUTOMATOR, locator_config['android']) 