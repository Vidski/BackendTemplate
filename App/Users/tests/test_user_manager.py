from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user_successfully(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normaluser@test.com',
            first_name='test_name',
            last_name='test_last_name',
            password='test_password',
        )
        self.assertEqual(user.email, 'normaluser@test.com')
        self.assertTrue(user.is_active)
        self.assertIsNone(user.username)

    def test_create_user_fails_without_data(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_create_user_fails_with_email_and_without_password(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='email@test.com', password="")

    def test_create_user_fails_with_email_without_password(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='', password='foo')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com',
            first_name='test_name',
            last_name='test_last_name',
            password='test_password',
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_verified)
        self.assertIsNone(admin_user.username)

    def test_create_superuser_fails_without_data(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_superuser()

    def test_create_superuser_fails_with_email_and_without_password(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                email='adminemail@test.com', password=""
            )

    def test_create_superuser_fails_with_email_without_password(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            User.objects.create_superuser(email='', password='foo')
