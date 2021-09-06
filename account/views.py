from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.crypto import get_random_string

import chat
from .serializers import *
from .models import User


def index(request):
    return render(request, 'account/register.html')

class UsersListView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserListSerializer


class UserCreateView(APIView):
    queryset = User.objects.all()
    permission_classes = (
        permissions.AllowAny,
    )

    def _send_activation_code(self, user):
        send_mail(
            'Thank you for joining to our messenger',
            f'Your activation code is: {user.activation_code}',
            'amann.sabyr@gmail.com',
            [{user.email}],
        )
        return None

    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            dict_data = dict(serializer.validated_data)
            User.objects.create_user(username=dict_data.get('username'),
                                     password=dict_data.get('password'),
                                     email=dict_data.get('email'))
            self._send_activation_code(User.objects.get(username=dict_data.get('username')))
            return render(request, 'account/activate.html')
        return Response('Account wasn\'t created')


class UserActivateView(APIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        data = request.data
        user = request.user
        serializer = UserActivationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return chat.views.index(request)
        return Response('Check you\'re data!')


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer


class UserInfoUpdateView(APIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = UserInfoUpdateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response('Info was successfully updated', status=200)
        return Response('Info wasn\'t updated')


class UserChangePasswordView(APIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = UserChangePasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response('Password was successfully updated!', status=200)
        return Response('Password wasn\'t updated')
