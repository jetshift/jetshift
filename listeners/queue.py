from jetshift_core.helpers.listeners import *

channel = os.environ.get('REDIS_EVENT_CHANNEL', 'test')

def handle_message(message):
    print('Queue listener received message:', message)

    if message.get('type') == 'message':
        params = (message.get('data'),)

        # Send the job to the RQ queue
        redis_conn = redis_connection()
        rq_queue = Queue(connection=redis_conn)
        rq_queue.enqueue(run_multi_process, send_discord_message, *params)


def run_multi_process(function_to_call, *params):
    try:
        p = multiprocessing.Process(target=function_to_call, args=params)
        p.start()
        p.join()
        logger.info("Process completed")
    except Exception as e:
        logger.error(f"An error occurred while running the process: {str(e)}")


def main():
    try:
        listen(channel, handle_message)
    except Exception as e:
        logger.error(f"Failed to start listener: {e}", exc_info=True)


if __name__ == '__main__':
    main()
