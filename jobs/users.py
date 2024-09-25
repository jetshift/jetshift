from config.luigi import luigi, local_scheduler
from jetshift_core.tasks.mysql_clickhouse_insert import BaseTask


class UsersETL(BaseTask):
    table_name = 'users'


def main():
    luigi.build([UsersETL(
        live_schema=True,
        truncate_table=False,
        primary_id_column='id',
        extract_offset=0,
        extract_limit=5,
        # extract_chunk_size=5,
        load_chunk_size=5
    )], local_scheduler=local_scheduler)


if __name__ == '__main__':
    main()
