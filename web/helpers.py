import time
from web import socketio


def broadcast_message():
    time.sleep(2)  # Wait for 2 seconds
    socketio.emit('event', {'message': 'Hello, all clients!'})
    return "Message broadcasted!"
