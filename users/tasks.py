from datetime import timedelta, date
from celery import shared_task

from users.models import User


@shared_task
def check_user_activity():
    """блокировка пользователей неактивных более 30 дней"""

    users = User.objects.filter(is_active=True)
    today = date.today()
    for user in users:
        if user.last_login:
            if today - user.last_login.date() > timedelta(days=30):
                user.is_active = False
                user.save()
