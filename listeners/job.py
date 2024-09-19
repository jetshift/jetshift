from jetshift_core.helpers.listeners import *

channel = os.environ.get('REDIS_EVENT_CHANNEL', 'test')


def handle_message(message):
    print('Job listener received message:', message)

    if message.get('type') == 'message':
        event_type = message.get('type')  # subscribe, message, unsubscribe
        job = message.get('data')
        print(f'Received job event: {job}. Type: {event_type}')

        # Jobs
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


def main():
    try:
        listen(channel, handle_message)
    except Exception as e:
        logger.error(f"Failed to start listener: {e}", exc_info=True)


if __name__ == '__main__':
    main()
