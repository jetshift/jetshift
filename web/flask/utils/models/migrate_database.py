from web.flask.databases.models import MigrateDatabase


def get_database_list():
    databases = MigrateDatabase.query.order_by(MigrateDatabase.id.desc())

    data = [
        {
            "id": db_entry.id,
            "title": db_entry.title,
            "source_db": db_entry.source_db.title,
            "target_db": db_entry.target_db.title,
            "logs": db_entry.logs,
            "status": db_entry.status,
            "created_at": db_entry.created_at.isoformat(),
            "updated_at": db_entry.updated_at.isoformat(),
        }
        for db_entry in databases
    ]

    return data
