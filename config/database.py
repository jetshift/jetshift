import json
import os
from dotenv import load_dotenv

load_dotenv()
secrets_json = os.environ.get('SECRETS_JSON')


def mysql():
    if secrets_json:
        secrets = json.loads(secrets_json)
        host = secrets.get('mysql_host')
        user = secrets.get('mysql_user')
        password = secrets.get('mysql_password')
    else:
        host = os.environ.get('MYSQL_HOST')
        user = os.environ.get('MYSQL_USER')
        password = os.environ.get('MYSQL_PASSWORD')

    database = os.environ.get('MYSQL_DATABASE', 'electronicfirst')

    return {
        'host': host,
        'user': user,
        'password': password,
        'database': database
    }


def clickhouse():
    if secrets_json:
        secrets = json.loads(secrets_json)
        host = secrets.get('clickhouse_host')
        password = secrets.get('clickhouse_password')
    else:
        host = os.environ.get('CLICKHOUSE_HOST')
        password = os.environ.get('CLICKHOUSE_PASSWORD')

    user = os.environ.get('CLICKHOUSE_USER', 'default')
    database = os.environ.get('CLICKHOUSE_DATABASE', 'default')
    port = os.environ.get('CLICKHOUSE_PORT', 9440)  # 9440 for secure connections, 9000 for local
    secure = os.environ.get('CLICKHOUSE_SECURE', 'True').lower() in ['true', '1']

    return {
        'host': host,
        'user': user,
        'password': password,
        'database': database,
        'port': port,
        'secure': secure
    }
