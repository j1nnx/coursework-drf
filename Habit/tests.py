from datetime import time
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from .models import Habit
from .serializers import HabitSerializers


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email='test@example.com',
            telegram_id='123456789'
        )
        self.habit_data = {
            'user': self.user,
            'place': 'Home',
            'time': time(10, 0),
            'action': 'Read a book',
            'is_nice': False,
            'periodicity': 1,
            'duration': 60,
            'is_public': False
        }
        self.habit = Habit.objects.create(**self.habit_data)

    def test_create_habit(self):
        self.assertEqual(self.habit.place, self.habit_data['place'])
        self.assertEqual(self.habit.time, self.habit_data['time'])
        self.assertEqual(self.habit.action, self.habit_data['action'])
        self.assertEqual(self.habit.is_nice, self.habit_data['is_nice'])
        self.assertEqual(self.habit.periodicity, self.habit_data['periodicity'])
        self.assertEqual(self.habit.duration, self.habit_data['duration'])
        self.assertEqual(self.habit.is_public, self.habit_data['is_public'])

    def test_habit_str(self):
        expected_str = f'{self.habit.action} в {self.habit.time} в {self.habit.place}'
        self.assertEqual(str(self.habit), expected_str)

    def test_validation_reward_and_related_habit(self):
        nice_habit = Habit.objects.create(
            user=self.user,
            place='Home',
            time=time(10, 0),
            action='Meditation',
            is_nice=True,
            periodicity=1,
            duration=60
        )
        habit = Habit(
            user=self.user,
            place='Home',
            time=time(10, 0),
            action='Read a book',
            is_nice=False,
            related_habit=nice_habit,
            reward='Watch TV',
            periodicity=1,
            duration=60
        )
        with self.assertRaises(Exception):
            habit.full_clean()

    def test_validation_duration(self):
        habit = Habit(
            user=self.user,
            place='Home',
            time=time(10, 0),
            action='Read a book',
            is_nice=False,
            periodicity=1,
            duration=121,
            is_public=False
        )
        with self.assertRaises(Exception):
            habit.full_clean()