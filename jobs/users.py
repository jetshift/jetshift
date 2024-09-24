from config.luigi import luigi, local_scheduler
from jetshift_core.tasks.mysql_clickhouse_insert import BaseTask


class UsersETL(BaseTask):
    table_name = 'users'


def main():
    luigi.build([UsersETL(chunk_size=15)], local_scheduler=local_scheduler)


if __name__ == '__main__':
    main()
