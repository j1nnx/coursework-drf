import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_creation_success(self):
        """Тест успешного создания пользователя"""
        email = "testuser@example.com"
        password = "testpass123"
        username = "testuser"

        user = User.objects.create_user(
            email=email,
            password=password,
            username=username
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))  # Проверяем, что пароль установлен корректно
        self.assertTrue(user.is_active)  # По умолчанию пользователь активен
        self.assertFalse(user.is_staff)  # Не персонал
        self.assertFalse(user.is_superuser)  # Не суперпользователь
        self.assertEqual(str(user), email)  # Проверяем строковое представление


# Запуск теста (опционально, если запускаете вручную)
if __name__ == "__main__":
    unittest.main()