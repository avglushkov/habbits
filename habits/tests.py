from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import datetime
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com", tg_chat_id=403235643)
        self.pleasant_habit = Habit.objects.create(user=self.user,
                                                   habit_place='приятное тестовое место',
                                                   habit_action='приятное тестовое действие',
                                                   execution_time=60,
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
        url = reverse("habits:habit_detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("habit_place"), self.habit.habit_place)

    def test_habit_update(self):
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {"habit_place": "updated place"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("habit_place"), "updated place")
    def tearDown(self):
        pass

#
#
# def test_lesson_delete(self):
#     url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
#     response = self.client.delete(url)
#     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#     self.assertEqual(Lesson.objects.all().count(), 0)
#
#
# def test_lesson_list(self):
#     url = reverse("lms:lesson-list")
#     response = self.client.get(url)
#     data = response.json()
#     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     result = {
#         "count": 1,
#         "next": None,
#         "previous": None,
#         "results": [
#             {
#                 "id": self.lesson.pk,
#                 "name": self.lesson.name,
#                 "description": self.lesson.description,
#                 "preview": None,
#                 "video_link": None,
#                 "course": self.course.pk,
#                 "owner": self.user.pk
#             }
#         ]
#     }
#     self.assertEqual(data, result)
