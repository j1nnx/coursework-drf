import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from Habit.models import Habit
from Habit.serializers import HabitSerializers  # Предполагаем правильное имя
import factory


# Фабрики
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habit

    user = factory.SubFactory(UserFactory)
    place = "Дом"
    time = "08:00:00"
    action = "Пить воду"
    is_nice = False
    periodicity = 1
    duration = 60
    is_public = False


# Фикстуры
@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def habit(user):
    return HabitFactory(user=user)


@pytest.fixture
def public_habit():
    return HabitFactory(is_public=True)


# Твои исходные тесты
@pytest.mark.django_db
def test_habit_list_unauthenticated(api_client):
    url = reverse('habit-list-create')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_public_habit_list_unauthenticated(api_client):
    url = reverse('public-habit-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
