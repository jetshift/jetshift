import os
from rq import Queue
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config.database import redis_connection
from config.logging import logger
from web.flask.utils.socket import socketio
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()


def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes and origins
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    # Initialize SocketIO with app
    socketio.init_app(app)

    # Register blueprints inside the function to avoid circular imports
    from web.flask.routes import main_bp
    from web.flask.api import api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # Import websocket handler
    import web.flask.websocket

    # Set up Redis connection and RQ queue
    job_queue = os.environ.get('JOB_QUEUE', 'False').lower() == 'true'
    if job_queue:
        try:
            logger.info('Setting up RQ queue')
            redis_conn = redis_connection()
            app.rq_queue = Queue(connection=redis_conn)
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            app.rq_queue = None
    else:
        app.rq_queue = None

    return app, socketio, db


# Create the app and expose it as a module-level variable
app, socketio, db = create_app()

if __name__ == "__main__":
    import eventlet

    eventlet.monkey_patch()

    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
