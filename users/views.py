
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError

from config.settings import EMAIL_HOST_USER

from users.models import User
from users.services import create_stripe_product, create_stripe_price, create_stripe_session
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'retrive':
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [~IsModerator | IsOwner]

        return super().get_permissions()


