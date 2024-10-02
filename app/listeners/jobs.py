from jetshift_core.helpers.listeners import *

channel = os.environ.get('REDIS_EVENT_CHANNEL', 'test')


def handle_message(message):
    print('Jobs listener received message:', message)

    if message.get('type') == 'message':
        redis_conn = redis_connection()
        rq_queue = Queue(connection=redis_conn)

        # Jobs
        jobs = {'time', 'ping'}

        for job in jobs:
            print(f'Queueing job: {job}')
            module_name = f'jobs.{job}'

            # Send the job to the RQ queue
            rq_queue.enqueue(run_job_in_new_process, module_name)


def main():
    try:
        listen(channel, handle_message)
    except Exception as e:
        logger.error(f"Failed to start listener: {e}", exc_info=True)


if __name__ == '__main__':
    main()
