from django.db import models
from django.conf import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True,
                             verbose_name='Пользователь')
    habit_place = models.CharField(max_length=100,
                                   verbose_name='Место')
    habit_time = models.TimeField(blank=True,
                                  null=True,
                                  verbose_name='Время')
    habit_action = models.CharField(blank=True,
                                    null=True,
                                    max_length=255,
                                    verbose_name='Действие')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True,
                                      verbose_name='Связанная привычка')
    period = models.SmallIntegerField(blank=True,
                                      null=True,
                                      verbose_name='Периодичность '
                                                   'повторения (дни)')
    prize = models.CharField(max_length=255,
                             blank=True,
                             null=True,
                             verbose_name='Вознаграждение')
    execution_time = models.SmallIntegerField(blank=True,
                                              null=True,
                                              verbose_name='Время на '
                                                           'выполнение '
                                                           '(секунды)')
    is_pleasant = models.BooleanField(default=False,
                                      verbose_name='Приятная привычка')
    is_public = models.BooleanField(default=True,
                                    verbose_name='Публичная привычка')

    def __str__(self):
        return self.habit_action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
