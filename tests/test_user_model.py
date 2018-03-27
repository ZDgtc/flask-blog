import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    # 测试是否已设置密码
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    # 测试是否无法获取原密码
    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    # 测试验证功能是否正常
    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    # 测试加盐是否随机
    def test_password_salts_are_random(self):
        u1 = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u1.password_hash != u2.password_hash)

