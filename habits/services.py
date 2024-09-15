import datetime
import json
import os

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from habits.tasks import send_tg_message


def get_period_and_initial_time(habit, period):
    """Получение даты начала отправки сообщений и периодичности"""

    schedule, created = IntervalSchedule.objects.get_or_create(every=habit.period, period=IntervalSchedule.DAYS)
    today = datetime.datetime.today()
    if datetime.datetime.now().time() > habit.habit_time:
        initial_time = datetime.datetime(year=today.year, month=today.month, day=today.day + period,
                                         hour=habit.habit_time.hour, minute=habit.habit_time.minute)
    else:
        initial_time = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=habit.habit_time.hour,
                                         minute=habit.habit_time.minute)
    return schedule, initial_time


def create_periodic_task(habit):
    """Создание периодической задачи по отправки уведомления в телеграмм"""

    schedule, initial_time = get_period_and_initial_time(habit, 1)
    PeriodicTask.objects.create(name=f'periodic_task_for_habit_{habit.pk}',
                                task='habits.tasks.send_tg_message',
                                interval=schedule,
                                start_time=initial_time,
                                args=json.dumps([habit.pk])
                                )


def update_periodic_task(habit):
    """Определение времени задания для следующей отправки"""

    schedule, initial_time = get_period_and_initial_time(habit, habit.period)
    task = PeriodicTask.objects.get(name=f'periodic_task_for_habit_{habit.pk}')
    task.interval = schedule
    task.start_time = initial_time
    task.save()


def delete_periodic_task(habit):
    """Удаление задания для отправленного сообщения"""

    task = PeriodicTask.objects.get(name=f'periodic_task_for_habit_{habit.pk}')
    task.delete()
