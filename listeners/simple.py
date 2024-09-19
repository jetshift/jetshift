from jetshift_core.helpers.listeners import *

channel = os.environ.get('REDIS_EVENT_CHANNEL', 'test')


def handle_message(message):
    print('Test listener received message:', message)


def main():
    try:
        listen(channel, handle_message)
    except Exception as e:
        logger.error(f"Failed to start listener: {e}", exc_info=True)


if __name__ == '__main__':
    main()
