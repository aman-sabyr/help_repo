from django.urls import path, include
from django.contrib import admin

from chat import views

urlpatterns = [
    path('chat/', include('chat.urls', namespace='chat')),
    path('api/v1/account/', include('account.urls')),
]