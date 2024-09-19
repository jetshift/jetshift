import json
import os
from dotenv import load_dotenv

load_dotenv()
secrets_json = os.environ.get('SECRETS_JSON')


def load_secrets():
    return json.loads(secrets_json) if secrets_json else {}


def get_env_var(key, default=None):
    return os.environ.get(key, default)


def redis_connection():
    from config.logging import logger
    from redis import Redis

    try:
        secrets = load_secrets()
        host = secrets.get('REDIS_HOST', os.environ.get('REDIS_HOST', 'localhost'))
        port = secrets.get('REDIS_PORT', os.environ.get('REDIS_PORT', 6379))
        password = secrets.get('REDIS_PASSWORD', os.environ.get('REDIS_PASSWORD', None))
        ssl = secrets.get('REDIS_SSL', os.environ.get('REDIS_SSL', 'False')).lower() in ['true', '1']

        redis_conn = Redis(
            host=host,
            port=int(port),
            password=password,
            ssl=ssl,
            decode_responses=True
        )
    except Exception as e:
        logger.error(f'Error setting up Redis connection: {e}')
        redis_conn = None

    return redis_conn


def mysql():
    secrets = load_secrets()
    return {
        'host': secrets.get('MYSQL_HOST', get_env_var('MYSQL_HOST')),
        'user': secrets.get('MYSQL_USER', get_env_var('MYSQL_USER')),
        'password': secrets.get('MYSQL_PASSWORD', get_env_var('MYSQL_PASSWORD')),
        'database': secrets.get('MYSQL_DATABASE', get_env_var('MYSQL_DATABASE', 'jetshift')),
    }


def clickhouse():
    secrets = load_secrets()
    return {
        'host': secrets.get('CLICKHOUSE_HOST', get_env_var('CLICKHOUSE_HOST')),
        'user': secrets.get('CLICKHOUSE_USER', get_env_var('CLICKHOUSE_USER', 'default')),
        'password': secrets.get('CLICKHOUSE_PASSWORD', get_env_var('CLICKHOUSE_PASSWORD')),
        'database': secrets.get('CLICKHOUSE_DATABASE', get_env_var('CLICKHOUSE_DATABASE', 'default')),
        'port': secrets.get('CLICKHOUSE_PORT', get_env_var('CLICKHOUSE_PORT', 9440)),
        'secure': secrets.get('CLICKHOUSE_SECURE', get_env_var('CLICKHOUSE_SECURE', 'True')).lower() in ['true', '1']
    }
