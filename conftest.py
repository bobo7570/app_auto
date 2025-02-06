import pytest
from utils.driver import AppiumDriver
from config import load_accounts

# 加载账号配置
ACCOUNTS = load_accounts()

@pytest.fixture(scope="session")
def appium_driver():
    """Pytest fixture：提供Appium驱动实例（会话级）"""
    driver = AppiumDriver.get_driver(platform="ios")
    yield driver  # 测试用例执行前返回驱动实例
    AppiumDriver.quit_driver()  # 测试结束后退出驱动

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest钩子：测试报告生成处理"""
    outcome = yield
    report = outcome.get_result()
    
    # 测试失败时自动截图
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('appium_driver')
        if driver:
            page = BasePage(driver)
            # 生成带测试标识的截图
            page.take_screenshot(f"failure_{item.nodeid}") 

@pytest.fixture(scope="module")
def account_loader(request):
    """动态获取测试模块需要的账号类型"""
    marker = request.node.get_closest_marker("account_type")
    account_type = marker.args[0] if marker else "basic_user"
    return ACCOUNTS[account_type]

@pytest.fixture
def logged_in_user(appium_driver, account_loader):
    """带权限检查的登录fixture"""
    from pages.login_page import LoginPage
    
    login_page = LoginPage(appium_driver)
    account_data = account_loader
    
    # 执行登录
    login_page.login(account_data)
    
    # 权限验证
    required_perms = getattr(request.module, "REQUIRED_PERMISSIONS", [])
    if not login_page.check_permission(required_perms):
        pytest.skip("账号权限不足")
    
    yield account_data
    
    # 退出登录
    login_page.logout() 