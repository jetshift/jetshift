import json
import os
from dotenv import load_dotenv

load_dotenv()
secrets_json = os.environ.get('SECRETS_JSON')


def load_secrets():
    return json.loads(secrets_json) if secrets_json else {}


def get_env_var(key, default=None):
    return os.environ.get(key, default)


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
