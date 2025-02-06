import pytest
from pages.login_page import LoginPage

@pytest.fixture
def logged_in_user(appium_driver):
    """好友模块前置条件：已登录用户"""
    login_page = LoginPage(appium_driver)
    login_page.login("test_user", "password123")
    yield
    login_page.logout() 