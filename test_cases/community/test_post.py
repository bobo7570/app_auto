import pytest

@pytest.mark.account_type("community_admin")
class TestCommunityPost:
    REQUIRED_PERMISSIONS = ["post"]
    
    def test_create_post(self, logged_in_user):
        """社区管理账号发帖测试"""
        # 使用community_admin账号执行操作
        ...
        
    def test_delete_post(self, logged_in_user):
        """删除帖子测试"""
        ... 