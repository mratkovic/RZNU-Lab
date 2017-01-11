from django.shortcuts import render, redirect
from haikunator.haikunator import Haikunator
from .models import Room


def home(request):
    return render(request, "chat/home.html")


def join_room(request):
    label = request.GET.get('room_name', '')
    if not label:
        label = Haikunator().haikunate()
    return redirect(chat_room, label=label)


def chat_room(request, label):
    room, created = Room.objects.get_or_create(label=label)
    return render(request, "chat/chat.html", {
        'room': room,
        'messages': room.messages.order_by('timestamp'),
    })