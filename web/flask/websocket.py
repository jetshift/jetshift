from web.flask import socketio

# Handle incoming WebSocket messages
@socketio.on('message')
def handle_message(message):
    print(f"Received message: {message}")
    socketio.emit('response', f"Server says: {message}")

# Handle custom WebSocket events
@socketio.on('client_event')
def handle_custom_event(data):
    print(f"Received custom event: {data}")
    socketio.emit('custom_response', {"status": "OK", "data": data})
