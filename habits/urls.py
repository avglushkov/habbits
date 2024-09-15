from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from habits.models import Habit
from habits.views import HabitCreateAPIView, HabitUpdateAPIView, HabitDestroyAPIView, HabitListAPIView, \
    HabitRetrieveAPIView, PublicHabitListAPIView, PublicHabitRetrieveAPIView

from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path('', HabitListAPIView.as_view(), name='habit_list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
    path('public/', PublicHabitListAPIView.as_view(), name='public_habit'),
    path('public/<int:pk>/', PublicHabitRetrieveAPIView.as_view(), name='public_habit_detail'),
]
