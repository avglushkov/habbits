from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from habits.apps import HabbitsConfig


app_name = HabbitsConfig.name

 # router = DefaultRouter()
 # router.register(r'habits', HViewSet, basename='users')

urlpatterns = [

                  # path('register/', UserCreateAPIView.as_view(), name='register'),
                  # path('login/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='login'),
                  # path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
                  #
              ] #+ router.urls
