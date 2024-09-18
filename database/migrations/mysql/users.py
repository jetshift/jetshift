from jetshift_core.utils.database.sqlalchemy_mysql import *
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func

# Define table
table = Table(
    'users', metadata,
    Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('created_at', DateTime, nullable=False, server_default=func.now())
)


def main(fresh=None):
    create_table(table, fresh)


if __name__ == "__main__":
    main()
