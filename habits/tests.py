from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    time = '17:31:00'

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            action='Habit_test_1',
            periodicity=1,
            lead_time='10',
            time=self.time,
            is_public=True
        )

        self.habit_pleasurable = Habit.objects.create(
            user=self.user,
            action='Habit_test_1_pleasurable',
            periodicity=1,
            lead_time='10',
            time=self.time,
            is_pleasurable=True,
        )

    def test_create_habit(self):
        """Тестирование создания привычки"""
        habit = {
            "action": "Habit_test_2",
            "lead_time": 10,
            "periodicity": 1,
            "time": self.time
        }
        response = self.client.post(
            '/habit/create/',
            data=habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": response.data['id'],
                "place": None,
                "time": self.time,
                "periodicity": 1,
                "action": "Habit_test_2",
                "is_pleasurable": False,
                "associated_habit": None,
                "reward": None,
                "lead_time": 10,
                "is_public": False
            }
        )

        self.assertTrue(
            Habit.objects.all().exists()
        )

    def test_create_habit_validation_error_1(self):
        """
        Тестирование валидации при создании привычки
        Валидатор 1: Проверка времени на выполнение привычки
        """
        habit = {
            "action": "Habit_test_2",
            "lead_time": 121,
            "periodicity": 1,
            "time": self.time
        }
        response = self.client.post(
            '/habit/create/',
            data=habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Время на выполнение должно быть не больше 120 минут"
                ]
            }
        )

    def test_create_habit_validation_error_2(self):
        """
        Тестирование валидации при создании привычки
        Валидатор 2: Проверка периодичности выполнения в днях
        """
        habit = {
            "action": "Habit_test_2",
            "lead_time": 10,
            "periodicity": 8,
            "time": self.time
        }
        response = self.client.post(
            '/habit/create/',
            data=habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Периодичность выполнения должна быть не реже, чем 1 раз за 7 дней"
                ]
            }
        )

    def test_create_habit_validation_error_3(self):
        """
        Тестирование валидации при создании привычки
        Валидатор 3: Проверка, что одновременно не назначено вознаграждение и связанная привычка
        """
        habit = {
            "action": "Habit_test_2",
            "lead_time": 10,
            "periodicity": 7,
            "time": self.time,
            "associated_habit": self.habit_pleasurable.id,
            "reward": "Test"
        }
        response = self.client.post(
            '/habit/create/',
            data=habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Нельзя назначить вознаграждение и связанную привычку одновременно"
                ]
            }
        )

    def test_create_habit_validation_error_4(self):
        """
        Тестирование валидации при создании привычки
        Валидатор 4: Проверка, что у приятной привычки не назначено вознаграждение или связанная привычка
        """
        habit = {
            "action": "Habit_test_2",
            "lead_time": 10,
            "periodicity": 7,
            "time": self.time,
            "is_pleasurable": True,
            "associated_habit": self.habit_pleasurable.id
        }
        response = self.client.post(
            '/habit/create/',
            data=habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Нельзя назначить вознаграждение или связанную привычку для приятной привычки"
                ]
            }
        )

    def test_create_habit_validation_error_5(self):
        """
        Тестирование валидации при создании привычки
        Валидатор 5: Проверка, что связанная привычка является приятной
        """
        habit = {
            "action": "Habit_test_2",
            "lead_time": 10,
            "periodicity": 7,
            "time": self.time,
            "associated_habit": self.habit.id
        }
        response = self.client.post(
            '/habit/create/',
            data=habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Связанная привычка должна быть приятной"
                ]
            }
        )

    def test_retrieve_habit(self):
        """Тестирование просмотра привычки"""

        response = self.client.get(
            f'/habit/{self.habit.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.habit.id,
                'place': None,
                'time': '17:31:00',
                'periodicity': 1,
                'action': 'Habit_test_1',
                'is_pleasurable': False,
                'associated_habit': None,
                'reward': None,
                'lead_time': 10,
                'is_public': True
            }
        )

    def test_list_habit(self):
        """Тестирование вывода списка привычек"""

        response = self.client.get(
            '/habit/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 2,
             'next': None,
             'previous': None,
             'results':
                 [
                     {
                         'id': self.habit.id,
                         'place': None,
                         'time': '17:31:00',
                         'periodicity': 1,
                         'action': 'Habit_test_1',
                         'is_pleasurable': False,
                         'associated_habit': None,
                         'reward': None,
                         'lead_time': 10,
                         'is_public': True
                     },
                     {
                         'id': self.habit_pleasurable.id,
                         'place': None,
                         'time': '17:31:00',
                         'periodicity': 1,
                         'action': 'Habit_test_1_pleasurable',
                         'is_pleasurable': True,
                         'associated_habit': None,
                         'reward': None,
                         'lead_time': 10,
                         'is_public': False
                     }
                 ]
             }
        )

    def test_public_list_habit(self):
        """Тестирование вывода списка публичных привычек"""

        response = self.client.get(
            '/habit/public_list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results':
                 [
                     {
                         'place': None,
                         'time': '17:31:00',
                         'periodicity': 1,
                         'action': 'Habit_test_1',
                         'is_pleasurable': False,
                         'associated_habit': None,
                         'reward': None,
                         'lead_time': 10
                     }
                 ]
             }
        )

    def test_update_habit(self):
        """Тестирование обновления привычки"""

        habit = {
            "action": "Habit_test_1_update",
            "lead_time": 10,
            "periodicity": 1,
            "time": self.time,
            "is_public": True
        }

        response = self.client.patch(
            f'/habit/{self.habit.id}/update/',
            data=habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.habit.id,
                'place': None,
                'time': '17:31:00',
                'periodicity': 1,
                'action': 'Habit_test_1_update',
                'is_pleasurable': False,
                'associated_habit': None,
                'reward': None,
                'lead_time': 10,
                'is_public': True
            }
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки"""

        response = self.client.delete(
            f'/habit/{self.habit.id}/delete/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
