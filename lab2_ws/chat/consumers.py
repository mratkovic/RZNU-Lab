import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room


@channel_session
def ws_connect(message):
    prefix, label = message['path'].strip('/').split('/')
    room = Room.objects.get(label=label)
    Group(Room.room_id_from_label(label)).add(message.reply_channel)
    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Room.objects.get(label=label)
    data = json.loads(message['text'])
    if data:
        m = room.messages.create(**data)
        Group(Room.room_id_from_label(label)).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        _ = Room.objects.get(label=label)
        Group(Room.room_id_from_label(label)).discard(message.reply_channel)

    except (KeyError, Room.DoesNotExist):
        pass
