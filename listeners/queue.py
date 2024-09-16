from dotenv import load_dotenv
from jetshift_core.helpers.common import run_job_in_new_process, send_discord_message
from rq import Queue

from config.database import redis_connection
from config.logging import logger
from jetshift_core.helpers.listeners import listen

# Load environment variables
load_dotenv()


def handle_message(message):
    print('Test listener received message:', message)

    # Send the job to the RQ queue
    redis_conn = redis_connection()
    rq_queue = Queue(connection=redis_conn)
    rq_queue.enqueue(run_job_in_new_process, send_discord_message('Test message from listener'))


def main():
    try:
        listen('queue-channel', handle_message)
    except Exception as e:
        logger.error(f"Failed to start listener: {e}", exc_info=True)


if __name__ == '__main__':
    main()
