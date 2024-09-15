from celery import shared_task
from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN
from datetime import datetime, timedelta
import requests
from habits.models import Habit
from users.models import User


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
        requests.get(f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage', params=params)


# @shared_task
# def send_tg_message():
#     habits = Habit.objects.all()
#     users = User.objects.all()
#     for user in users:
#         if user.tg_chat_id:
#             for habit in habits:
#                 habit_start_time = habit.habit_time.replace(second=0, microsecond=0)
#                 habit_time_now =datetime.now(pytz.timezone(TIME_ZONE)).replace(second=0, microsecond=0)
#                 if habit_start_time == habit_time_now:
#                     if habit.is_pleasant:
#                         message = (f"Напоминаю, что Вам нужно {habit.habit_action} в {habit.habit_place}.\n"
#                                    f"На это вам дано {habit.execution_time} секунд\n")
#
#                         params = {
#                             "text": message,
#                             "chat_id": habit.user.tg_chat_id,
#                         }
#                         requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
#
#                     if habit.related_habit:
#                         message = (f"Напоминаю, что Вам нужно {habit.habit_action} в {habit.habit_place}.\n"
#                                    f"На это вам дано {habit.execution_time} секунд\n"
#                                    f"За это вы можете {habit.related_habit.action}")
#
#                         send_telegram_message(habit.user.tg_chat_id, message)
#
#                         params = {
#                                 "text": message,
#                                 "chat_id": habit.user.tg_chat_id,
#                             }
#                         requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
#                     if habit.prize:
#                         message = (f"Напоминаю, что Вам нужно {habit.habit_action} в {habit.habit_place}.\n"
#                                    f"На это Вам дано {habit.execution_time} секунд\n"
#                                    f"За это Вам полагается {habit.prize}")
#
#                         params = {
#                             "text": message,
#                             "chat_id": habit.user.tg_chat_id,
#                         }
#                         requests.get(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)
#
#
#                     habit.time = datetime.now(pytz.timezone(TIME_ZONE)) + timedelta(days=habit.period)
#                     habit.save()
