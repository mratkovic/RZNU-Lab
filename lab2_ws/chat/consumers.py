import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room


@channel_session
def ws_connect(message):
    try:
        prefix, label = message['path'].strip('/').split('/')
        if prefix != 'chat':
            logging.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(label=label)

    except ValueError:
        logging.debug('invalid ws path=%s', message['path'])
        return

    except Room.DoesNotExist:
        logging.debug('ws room does not exist label=%s', label)
        return

    logging.debug('chat connect room=%s client=%s:%s', room.label, message['client'][0], message['client'][1])
    Group(Room.room_id_from_label(label)).add(message.reply_channel)
    message.channel_session['room'] = room.label


@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)

    except KeyError:
        logging.debug('no room in channel_session')
        return

    except Room.DoesNotExist:
        logging.debug('recieved message, but room does not exist label=%s', label)
        return

    try:
        data = json.loads(message['text'])

    except ValueError:
        logging.debug("ws message isn't json text=%s", message['text'])
        return

    if set(data.keys()) != set(('handle', 'message')):
        logging.debug("ws message unexpected format data=%s", data)
        return

    if data:
        logging.debug('chat message room=%s handle=%s message=%s', room.label, data['handle'], data['message'])
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
