import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from users.serializers import UserRegistrationSerializer
import factory


# Фабрика для CustomUser
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    telegram_id = factory.Sequence(lambda n: f"telegram{n}")
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


# Фикстуры
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


# Тесты для UserRegistrationView
@pytest.mark.django_db
def test_user_registration_success(api_client):
    url = reverse('user-registration')
    data = {
        "email": "newuser@example.com",
        "telegram_id": "telegram123",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert CustomUser.objects.filter(email="newuser@example.com").exists()
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['user']['email'] == "newuser@example.com"


@pytest.mark.django_db
def test_user_registration_password_mismatch(api_client):
    url = reverse('user-registration')
    data = {
        "email": "newuser@example.com",
        "telegram_id": "telegram123",
        "password": "testpass123",
        "password_confirm": "differentpass"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Пароли не совпадают" in str(response.data)


# Тесты для UserLoginView
@pytest.mark.django_db
def test_user_login_success(api_client, user):
    url = reverse('user-login')
    data = {
        "email": user.email,
        "password": "testpass123"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_user_login_invalid_password(api_client, user):
    url = reverse('user-login')
    data = {
        "email": user.email,
        "password": "wrongpass"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Неверный пароль" in response.data['error']


@pytest.mark.django_db
def test_user_login_nonexistent_user(api_client):
    url = reverse('user-login')
    data = {
        "email": "nonexistent@example.com",
        "password": "testpass123"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Пользователь не найден" in response.data['error']


# Тесты для TokenRefreshView
@pytest.mark.django_db
def test_token_refresh_success(api_client, user):
    refresh = RefreshToken.for_user(user)
    url = reverse('token-refresh')
    data = {"refresh": str(refresh)}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data


@pytest.mark.django_db
def test_token_refresh_invalid_token(api_client):
    url = reverse('token-refresh')
    data = {"refresh": "invalidtoken"}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Недействительный токен" in response.data['error']


@pytest.mark.django_db
def test_token_refresh_missing_token(api_client):
    url = reverse('token-refresh')
    data = {}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Токен не предоставлен" in response.data['error']


# Тест для UserRegistrationSerializer
@pytest.mark.django_db
def test_user_serializer_validation():
    data = {
        "email": "testuser@example.com",
        "telegram_id": "telegram123",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    serializer = UserRegistrationSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['email'] == "testuser@example.com"