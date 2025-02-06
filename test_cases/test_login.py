import pytest
from pages.login_page import LoginPage

class TestLogin:
    """登录功能测试用例集合"""
    
    @pytest.mark.parametrize("username,password", [
        ("valid_user", "correct_pwd"),  # 有效账号测试
        ("invalid_user", "wrong_pwd")   # 无效账号测试
    ])
    def test_user_login(self, appium_driver, username, password):
        """用户登录测试
        Args:
            appium_driver: 通过fixture获取的驱动实例
            username: 测试用户名
            password: 测试密码
        """
        login_page = LoginPage(appium_driver)
        # 执行登录操作
        login_page.input_username(username)
        login_page.input_password(password)
        login_page.click_login_button()
        
        # 验证结果
        if "valid" in username:
            assert login_page.is_login_success()  # 验证登录成功
        else:
            assert login_page.get_error_message() == "账号或密码错误"  # 验证错误提示 