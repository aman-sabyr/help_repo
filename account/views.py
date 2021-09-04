import json

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import generic
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import User


class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(APIView):
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        print(data)
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            dict_data = dict(serializer.validated_data)
            print(dict_data)
            User.objects.create_user(username=dict_data.get('username'),
                                     password=dict_data.get('password'))
        return Response('Account was successfully created', status=201)


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer


class UserInfoUpdateView(APIView):
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        serializer = UserInfoUpdateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response('Info was successfully updated', status=200)



