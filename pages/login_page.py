# 导入类型提示相关模块
from typing import Dict, Any
# 导入页面基类
from .base_page import BasePage
# 导入移动端定位方式
from appium.webdriver.common.mobileby import MobileBy
from config import load_locators

class LoginPage(BasePage):
    """登录页面对象模型，封装所有登录相关操作"""
    
    # 元素定位器配置区域-----------------------------------------
    
    # 用户名输入框定位器（使用iOS的accessibility_id定位方式）
    USERNAME_INPUT = (MobileBy.ACCESSIBILITY_ID, "username_input")
    # 密码输入框定位器（使用iOS的accessibility_id定位方式）
    PASSWORD_INPUT = (MobileBy.ACCESSIBILITY_ID, "password_input")
    # 登录按钮定位器（使用iOS的accessibility_id定位方式）
    LOGIN_BUTTON = (MobileBy.ACCESSIBILITY_ID, "login_btn")

    def load_locators(self):
        """加载登录页面定位配置"""
        return load_locators()['login_page']
    
    def input_username(self, text: str):
        """使用动态定位器输入用户名"""
        locator = self.get_locator('username_input')
        self.safe_input(locator, text)

    def login(self, account_data: Dict[str, Any]):
        """
        执行完整登录流程
        :param account_data: 包含登录凭证的字典，格式为 {'username': str, 'password': str}
        """
        # 在用户名输入框安全输入（带清除功能）
        self.safe_input(self.USERNAME_INPUT, account_data['username'])
        # 在密码输入框安全输入（带清除功能）
        self.safe_input(self.PASSWORD_INPUT, account_data['password'])
        # 点击登录按钮提交表单
        self.click(self.LOGIN_BUTTON)
        
    def check_permission(self, required_permissions: list) -> bool:
        """
        验证当前账号是否具有所需权限
        :param required_permissions: 需要验证的权限列表
        :return: 当拥有全部所需权限时返回True，否则返回False
        """
        # 从页面或接口获取当前账号的权限列表
        current_permissions = self.get_current_permissions()
        # 检查是否包含所有需要的权限
        return all(perm in current_permissions for perm in required_permissions) 