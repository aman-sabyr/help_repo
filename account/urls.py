from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserCreateView.as_view()),
    path('lists/', UsersListView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('update/', UserInfoUpdateView.as_view())
]