from web.flask import app, socketio
import eventlet

if __name__ == '__main__':
    eventlet.monkey_patch()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
