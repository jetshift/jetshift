import os
import platform
from rq import Queue
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from config.database import redis_connection
from config.logging import logger

# Load environment variables
load_dotenv()

# Environment-specific configurations
job_queue = os.environ.get('JOB_QUEUE', 'False') == 'True'
operating_system = os.environ.get('OS', platform.system().lower())

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app, cors_allowed_origins="*")

# Import and register blueprints
from web.routes import main_blueprint

app.register_blueprint(main_blueprint)

# Set up Redis connection and RQ queue
if job_queue is True:
    logger.info(f'JSetting up RQ queue')
    redis_conn = redis_connection()
    rq_queue = Queue(connection=redis_conn)
else:
    rq_queue = None
