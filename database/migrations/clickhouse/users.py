from sqlalchemy import Table, Column, func, DateTime
from jetshift_core.utils.database.sqlalchemy_clickhouse import *
from clickhouse_sqlalchemy import types, engines

# Define table
table = Table(
    'users', metadata,
    Column('id', types.Int32, primary_key=True),
    Column('name', types.String),
    Column('created_at', DateTime, nullable=False, server_default=func.now()),
    engines.MergeTree(order_by=['id'])
)


def main():
    create_table(table)


if __name__ == "__main__":
    main()
