from django.shortcuts import render

from account.models import User


def index(request):
    print(request.data)
    user = User.objects.get(username=request.data.get('username'))
    return render(request, 'chat/room. html')


def room(request, room_name):
    username = request.GET.get('user')

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': username
    })
