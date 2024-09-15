from celery import shared_task
from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN
import requests
from habits.models import Habit


@shared_task
def send_tg_message(habit_pk):
    habit = Habit.objects.get(pk=habit_pk)
    if habit.related_habit:

        message = (f"Напоминаю, что в {habit.habit_time.strftime('%H:%M')}\n"
                   f"вам нужно {habit.habit_action} в {habit.habit_place}.\n"
                   f"На это вам дано {habit.execution_time} секунд\n"
                   f"За это вы можете {habit.related_habit.habit_action}")
    else:

        message = (f"Напоминаю, что в {habit.habit_time.strftime('%H:%M')}\n"
                   f"вам нужно {habit.habit_action} в {habit.habit_place}.\n"
                   f"На это вам дано {habit.execution_time} секунд\n"
                   f"За это вам полагается {habit.prize}")

    if habit.user.tg_chat_id:
        chat_id = habit.user.tg_chat_id
        params = {'text': message, 'chat_id': chat_id}
        requests.get(f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage',
                     params=params)
