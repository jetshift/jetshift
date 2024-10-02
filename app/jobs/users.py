from config.luigi import luigi, local_scheduler
from jetshift_core.tasks.mysql_clickhouse_insert import BaseTask


class UsersETL(BaseTask):
    table_name = 'users'


def main():
    params = {
        'live_schema': False,
        'primary_id': 'id',
        # extract
        'extract_offset': 0,
        # 'extract_limit': 10,
        'extract_chunk_size': 100,
        # load
        'truncate_table': False,
        'load_chunk_size': 100,
        'sleep_interval': 1,
    }

    luigi.build([UsersETL(**params)], local_scheduler=local_scheduler)


if __name__ == '__main__':
    main()
