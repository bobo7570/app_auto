import pytest
from pages.friends_page import FriendsPage

@pytest.mark.account_type("basic_user")
class TestFriends:
    REQUIRED_PERMISSIONS = ["friend"]
    
    """好友功能测试集合"""
    
    @pytest.mark.parametrize("search_key", [
        "游戏好友123",
        "战队成员456"
    ])
    def test_search_and_add_friend(self, appium_driver, search_key):
        """搜索并添加好友测试"""
        friends_page = FriendsPage(appium_driver)
        
        # 执行操作
        friends_page.enter_add_friend_page()
        friends_page.search_friend(search_key)
        friends_page.send_add_request()
        
        # 验证结果
        assert friends_page.is_request_sent(), "好友请求发送失败"
        
    def test_accept_friend_request(self, appium_driver):
        """接受好友请求测试"""
        friends_page = FriendsPage(appium_driver)
        initial_count = friends_page.get_friend_count()
        
        friends_page.accept_first_request()
        
        assert friends_page.get_friend_count() == initial_count + 1, "好友数量未增加"

    def test_add_friend(self, logged_in_user):
        """基础用户添加好友测试"""
        ... 