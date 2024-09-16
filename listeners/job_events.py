import os
from dotenv import load_dotenv
from jetshift_core.helpers.common import run_job_in_new_process
from rq import Queue

from config.database import redis_connection
from config.logging import logger
from jetshift_core.helpers.listeners import listen

# Load environment variables
load_dotenv()


def handle_message(message):
    event_type = message.get('type')  # subscribe, message, unsubscribe
    job = message.get('data')
    print(f'Received job event: {job}. Type: {event_type}')

    # Send the job to the RQ queue
    jobs_directory = 'jobs'
    py_files = [
        f.replace('.py', '') for f in os.listdir(jobs_directory)
        if f.endswith('.py') and f != '__init__.py' and not f.startswith('test_')
    ]
    available_jobs = {f for f in py_files}

    if job in available_jobs:
        print(f'Queueing job: {job}')
        module_name = f'jobs.{job}'
        redis_conn = redis_connection()

        # Send the job to the RQ queue
        rq_queue = Queue(connection=redis_conn)
        rq_queue.enqueue(run_job_in_new_process, module_name)

    print('Test listener received message:', message)


def main():
    try:
        # Fetch the channel from environment variables
        channel = os.environ.get('REDIS_EVENT_CHANNEL', 'job-events')

        # Call the listener function with the custom handle_message
        listen(channel, handle_message)
    except Exception as e:
        logger.error(f"Failed to start listener: {e}", exc_info=True)


if __name__ == '__main__':
    main()
