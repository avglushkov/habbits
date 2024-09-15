from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import datetime
from habits.models import Habit
from habits.tasks import send_tg_message
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        """Добавление двух привычек для тестирования"""

        self.user = User.objects.create(email="test@test.com", tg_chat_id=403235643)
        self.pleasant_habit = Habit.objects.create(user=self.user,
                                                   habit_place='приятное тестовое место',
                                                   habit_action='приятное тестовое действие',
                                                   is_pleasant=True,
                                                   is_public=False
                                                   )
        self.habit = Habit.objects.create(user=self.user,
                                          habit_place='тестовое место',
                                          habit_time=datetime.datetime(2024, 1, 1, 00, 00, 00),
                                          habit_action='тестовое действие',
                                          related_habit=self.pleasant_habit,
                                          period=1,
                                          execution_time=60,
                                          is_pleasant=False,
                                          is_public=False
                                          )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тестирование создания привычки"""

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_time": "11:00",
                "habit_action": "New action",
                "period": 1,
                "execution_time": 60,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(user=self.user,
                                              habit_place='New habit place',
                                              habit_time='11:00:00',
                                              habit_action='New action',
                                              prize='Prize',
                                              period=1,
                                              execution_time=60,
                                              is_pleasant=False,
                                              is_public=False).count(), 1)

    def test_habit_retrive(self):
        """Тестирование вывода деталей привычки"""

        url = reverse("habits:habit_detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("habit_place"), self.habit.habit_place)

    def test_update_habit(self):
        """Тестирование изменения привычки"""

        self.client.post('/habits/create/',
                         data={
                             "habit_place": "тестовое место",
                             "habit_action": "тестовое действие",
                             "habit_time": "10:00",
                             "execution_time": 100,
                             "period": 1,
                             "prize": "test",
                             "is_pleasant": False,
                             "is_public": False})

        response = self.client.patch(reverse('habits:habit_update', args=(self.habit.pk + 1,)),
                                     data={
                                         "habit_place": "другое место",
                                         "habit_time": "00:00",
                                         "habit_action": "другое действие",
                                         "period": 2,
                                         "execution_time": 100,
                                         "prize": "другой приз"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             "id": self.habit.pk + 1,
                             "habit_place": "другое место",
                             "habit_time": "00:00:00",
                             "habit_action": "другое действие",
                             "period": 2,
                             "prize": "другой приз",
                             "execution_time": 100,
                             "is_pleasant": False,
                             "is_public": False,
                             "user": self.user.pk,
                             "related_habit": None})

    def test_list_habit(self):
        """Вывод списка привычек"""

        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.pleasant_habit.pk,
                        "habit_place": "приятное тестовое место",
                        "habit_time": None,
                        "habit_action": "приятное тестовое действие",
                        "period": None,
                        "prize": None,
                        "execution_time": None,
                        "is_pleasant": True,
                        "is_public": False,
                        "user": self.user.pk,
                        "related_habit": None
                    },

                    {
                        "id": self.habit.pk,
                        "habit_place": "тестовое место",
                        "habit_time": "00:00:00",
                        "habit_action": "тестовое действие",
                        "period": 1,
                        "prize": None,
                        "execution_time": 60,
                        "is_pleasant": False,
                        "is_public": False,
                        "user": self.user.pk,
                        "related_habit": self.pleasant_habit.pk
                    }
                ]
            }
        )

    def test_delete_habit(self):
        """Тестирование корректности удаления привычки"""

        self.client.post('/habits/create/',
                         data={
                             "habit_place": "тестовое место",
                             "habit_action": "тестовое действие",
                             "habit_time": "10:00",
                             "execution_time": 100,
                             "period": 1,
                             "prize": "test",
                             "is_pleasant": False,
                             "is_public": False})

        response = self.client.delete(reverse('habits:habit_delete', args=(self.habit.pk + 1,)), )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    ### Тестирование валидаторов
    def test_habit_time_validator(self):
        """Корректность валидатора ввода времени привычки"""

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_time": "11:00",
                "habit_action": "New action",
                "is_pleasant": True,
                "is_public": False}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Приятной привычке не требуется время (habit_time)']})

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "period": 1,
                "execution_time": 60,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"non_field_errors": ["Вы не заполнили время привычки (habit_time)"]})

    def test_habit_execution_validator(self):
        """Корректность валидатора ввода времени выполнения привычки"""

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "execution_time": 100,
                "habit_action": "New action",
                "is_pleasant": True,
                "is_public": False}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {'non_field_errors': [
                             'Для приятной привычки не нужно указывать время на выполнение (execution_time)']})

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "habit_time": "10:00",
                "execution_time": 130,
                "period": 1,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"non_field_errors": ["Время выполнения привычки не должно быть больше 120 секунд"]})

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "habit_time": "10:00",
                "execution_time": -1,
                "period": 1,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"non_field_errors": ["Время выполнения привычки должно быть больше 1 секунды"]})

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "habit_time": "10:00",
                "period": 1,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            "non_field_errors": ["Вы не заполнили поле с временем выполнения привычки (execution_time)"]})

    def test_habit_period_validator(self):
        """Корректность валидатора ввода времени выполнения привычки"""

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "period": 1,
                "habit_action": "New action",
                "is_pleasant": True,
                "is_public": False}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Для приятных привычек не нужна периодичность']})

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "habit_time": "10:00",
                "execution_time": 100,
                "period": 10,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"non_field_errors": ["Привычку нужно повторять не реже раза в неделю"]})

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "habit_time": "10:00",
                "execution_time": 100,
                "period": -1,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"non_field_errors": [
                             "Периодичность указана некорректно, она должна быть от одного до 7 дней"]})



        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "habit_time": "10:00",
                "execution_time": 100,
                "prize": "Prize",
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"non_field_errors": ["Вы не указали периодичность"]})

    def test_related_habit_validator(self):
        """Корректность валидатора связанной привычки"""

        url = reverse("habits:habit_create")
        data = {"habit_place": "New habit place",
                "habit_action": "New action",
                "habit_time": "10:00",
                "period": 1,
                "execution_time": 60,
                "related_habit": self.habit.pk,
                "is_pleasant": False,
                "is_public": False}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"non_field_errors": ["Полезные привычки можно связывать только с приятными"]})

    ### Тестирование отправки рассылок в телеграмм

    def test_send_tg_message(self):
        """Тестирование отправкти рассылки"""

        self.habit.related_habit = self.pleasant_habit
        self.habit.save()
        send_tg_message(self.habit.pk)

    def tearDown(self):
        pass
