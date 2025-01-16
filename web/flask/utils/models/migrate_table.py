from web.flask.databases.models import MigrateTable


def get_table_list():
    tables = MigrateTable.query.order_by(MigrateTable.id.desc())

    data = [
        {
            "id": db_entry.id,
            "title": db_entry.title,
            "source_db": db_entry.source_db.title,
            "target_db": db_entry.target_db.title,
            "source_tables": db_entry.source_tables,
            "target_tables": db_entry.target_tables,
            "logs": db_entry.logs,
            "status": db_entry.status,
            "created_at": db_entry.created_at.isoformat(),
            "updated_at": db_entry.updated_at.isoformat(),
        }
        for db_entry in tables
    ]

    return data
