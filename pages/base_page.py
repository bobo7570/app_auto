from appium.webdriver.webdriver import WebDriver, WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import Tuple, Optional
import time
from utils.locator_parser import LocatorParser
import logging

logger = logging.getLogger(__name__)

class ElementNotFoundError(Exception):
    """自定义元素未找到异常"""
    pass

class BasePage:
    """页面基类，封装通用操作方法"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # 获取当前平台类型（小写）
        self.platform = driver.desired_capabilities['platformName'].lower()
        # 显式等待实例
        self.wait = WebDriverWait(driver, 15)
        self.locators = self.load_locators()  # 加载定位配置
        
    def load_locators(self) -> dict:
        """加载定位配置（需子类实现），默认返回空字典"""
        return {}
    
    def get_locator(self, element_key: str) -> tuple:
        """
        获取跨平台定位器
        :param element_key: 定位配置中的元素键名
        :return: (定位方式, 定位表达式)
        """
        locator_config = self.locators.get(element_key)
        if not locator_config:
            raise KeyError(f"未找到 {element_key} 的定位配置")
            
        return LocatorParser.parse(locator_config, self.platform)
    
    def find_elements(self, locator: Tuple[str, str], timeout=15) -> list:
        """元素集合定位方法
        Args:
            locator: 定位器元组（定位方式, 定位表达式）
            timeout: 超时时间（秒）
        Returns:
            查找到的元素列表
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            self.take_screenshot("elements_not_found")
            raise NoSuchElementException(f"元素集合定位失败: {locator}")
    
    def find_element(self, locator: Tuple[str, str], timeout=15) -> WebElement:
        """增强版元素定位方法
        Args:
            locator: 定位器元组（定位方式, 表达式）
            timeout: 超时时间（秒）
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.take_screenshot("element_not_found")
            logger.error(f"元素定位失败: {locator}")
            raise ElementNotFoundError(f"元素定位失败: {locator}")
    
    def click(self, locator: Tuple[str, str], index: int = 0):
        """支持多元素点击"""
        elements = self.find_elements(locator)
        if len(elements) > index:
            elements[index].click()
        else:
            raise NoSuchElementException(f"第{index}个元素不存在: {locator}")
        
    def input_text(self, locator: tuple, text: str):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        
    def swipe_up(self, duration=500):
        """上滑操作"""
        size = self.driver.get_window_size()
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2
        self.driver.swipe(size['width']/2, start_y, size['width']/2, end_y, duration)
        
    def take_screenshot(self, name: str):
        """截图并保存"""
        self.driver.save_screenshot(f"screenshots/{name}.png")

    def clear_input(self, locator: Tuple[str, str]):
        """安全清空输入框"""
        element = self.find_element(locator)
        element.clear()
        if element.text != '':
            self.driver.execute_script('mobile: clearTextField', {'elementId': element.id})

    def safe_input(self, locator: Tuple[str, str], text: str):
        """防错输入方法，先清空输入框，再输入文本"""
        self.clear_input(locator)
        element = self.find_element(locator)
        if self.platform == 'ios':
            element.set_value(text)
        else:
            element.send_keys(text)

    def swipe(self, direction: str, duration: int = 500):
        """通用滑动方向控制"""
        screen_size = self.driver.get_window_size()
        x, y = screen_size['width'], screen_size['height']
        
        vectors = {
            'up':    (x*0.5, y*0.8, x*0.5, y*0.2),
            'down':  (x*0.5, y*0.2, x*0.5, y*0.8),
            'left':  (x*0.8, y*0.5, x*0.2, y*0.5),
            'right': (x*0.2, y*0.5, x*0.8, y*0.5)
        }
        self.driver.swipe(*vectors[direction], duration)

    def swipe_to_element(self, target_locator: Tuple[str, str], 
                        max_swipes: int = 5, direction: str = 'up'):
        """滑动直到找到元素"""
        for _ in range(max_swipes):
            if self.is_element_present(target_locator):
                return True
            self.swipe(direction)
        return False

    def long_press(self, locator: Tuple[str, str], duration: int = 1000):
        """长按操作"""
        element = self.find_element(locator)
        TouchAction(self.driver).long_press(element, duration=duration).perform()

    def drag_and_drop(self, source_loc: Tuple[str, str], target_loc: Tuple[str, str]):
        """拖拽元素"""
        source = self.find_element(source_loc)
        target = self.find_element(target_loc)
        TouchAction(self.driver).long_press(source).move_to(target).release().perform()

    def back(self):
        """通用返回操作"""
        if self.platform == 'android':
            self.driver.press_keycode(4)
        else:
            self.execute_script('mobile: pressButton', {'name': 'home'})

    def enter_game(self, game_name: str):
        """进入指定游戏（王者营地专用）"""
        self.click(self.GAME_ENTRY_LOCATOR)
        self.swipe_to_element((MobileBy.ANDROID_UIAUTOMATOR, 
                             f'new UiSelector().text("{game_name}")'))
        self.click(game_name)

    def virtual_joystick_control(self, direction: str, duration: int = 1000):
        """虚拟摇杆控制（需根据实际游戏调整坐标）"""
        base_x, base_y = 200, 500  # 摇杆基准坐标
        offset = {
            'up': (0, -100),
            'down': (0, 100),
            'left': (-100, 0),
            'right': (100, 0)
        }
        TouchAction(self.driver)\
            .press(x=base_x, y=base_y)\
            .move_to(x=base_x+offset[direction][0], y=base_y+offset[direction][1])\
            .wait(duration)\
            .release()\
            .perform()

    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """元素存在性检查"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_element_center(self, element: WebElement) -> Tuple[float, float]:
        """获取元素中心坐标"""
        location = element.location
        size = element.size
        return (location['x'] + size['width']/2, 
                location['y'] + size['height']/2)

    def get_current_permissions(self) -> list:
        """从用户界面或接口获取当前账号权限列表"""
        # 示例实现：从权限弹窗或用户信息接口获取
        permissions_element = self.find_element((MobileBy.ACCESSIBILITY_ID, "permissions_list"))
        return permissions_element.text.split(',') 