from django.test import TestCase
from .models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        """
        ユーザを作成できるか確認
        """
        User.objects.create(username='testuser', email='testuser@sample.com', nickname='test', password='test1234')
        User.objects.create(username='123456', email='123456@sample.com', nickname='1234', password='123456')
        User.objects.create(username='test0000', email='test0000@sample.com', nickname='test0000', password='pass0000')

    def test_get_user_information(self):
        """
        ユーザの情報を取得できるか確認
        """
        User.objects.create(username='test1234', email='test@sample.com', nickname='test', password='password1234')
        user = User.objects.get(username='test1234')
        self.assertEqual(user.email, 'test@sample.com')
        self.assertEqual(user.nickname, 'test')