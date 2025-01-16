import json
from datetime import datetime
from web.flask.main import app, db
from web.flask.databases.models import User, Database, MigrateDatabase, MigrateTable


def seed_data():
    # Seed users
    users = [
        User(username="john_doe", name="John Doe", email="john@example.com"),
        User(username="jane_smith", name="Jane Smith", email="jane@example.com")
    ]

    # Seed databases
    databases = [
        Database(
            id=1,
            title="SQLite 1",
            dialect="sqlite",
            type='source',
            database="jetshift.db",
            status=True,
            created_at=datetime.fromisoformat("2022-09-15T08:00:00"),
            updated_at=datetime.fromisoformat("2023-10-01T12:30:00")
        ),
        Database(
            id=2,
            title="MySQL 1",
            dialect="mysql",
            type='target',
            host="localhost",
            port=3306,
            username="root",
            password="",
            database="test",
            status=True,
            created_at=datetime.fromisoformat("2022-09-15T08:00:00"),
            updated_at=datetime.fromisoformat("2023-10-01T12:30:00")
        ),
        Database(
            id=3,
            title="Postgres 1",
            dialect="postgresql",
            type='target',
            host="localhost",
            port=5432,
            username="admin",
            password="securepass",
            database="test",
            status=True,
            created_at=datetime.fromisoformat("2022-09-01T12:00:00"),
            updated_at=datetime.fromisoformat("2023-09-01T15:30:00")
        )
    ]

    # Seed migrate databases
    migrate_databases = [
        MigrateDatabase(title="DBM Job 1", source_db_id=1, target_db_id=2),
    ]

    # Seed migrate tables
    migrate_tables = [
        MigrateTable(title="TM Job 1", source_db_id=1, target_db_id=2, source_tables=json.dumps(["users"])),
    ]

    # Add to session and commit
    with app.app_context():
        try:
            db.create_all()  # Ensure tables exist

            db.session.bulk_save_objects(databases)
            db.session.commit()  # Commit before adding related entries

            db.session.bulk_save_objects(migrate_databases)
            db.session.commit()

            db.session.bulk_save_objects(users + migrate_tables)
            db.session.commit()
            print("Data seeded successfully!")
        except Exception as e:
            print(f"An error occurred while seeding data: {e}")


if __name__ == "__main__":
    seed_data()
