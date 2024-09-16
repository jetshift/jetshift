from dotenv import load_dotenv
from config.logging import logger
from jetshift_core.helpers.listeners import listen

# Load environment variables
load_dotenv()


def handle_message(message):
    print('Test listener received message:', message)


def main():
    try:
        listen('test-channel', handle_message)
    except Exception as e:
        logger.error(f"Failed to start listener: {e}", exc_info=True)


if __name__ == '__main__':
    main()
