from datetime import datetime
from web.flask.main import app, db
from web.flask.databases.models import User, Database


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
            type='source',
            name="MySQL 1",
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="test",
            engine="mysql",
            status=True,
            created_at=datetime.fromisoformat("2022-09-15T08:00:00"),
            updated_at=datetime.fromisoformat("2023-10-01T12:30:00")
        ),
        Database(
            id=2,
            type='target',
            name="Postgres 1",
            host="localhost",
            port=5432,
            user="admin",
            password="securepass",
            database="test",
            engine="postgres",
            status=True,
            created_at=datetime.fromisoformat("2022-09-01T12:00:00"),
            updated_at=datetime.fromisoformat("2023-09-01T15:30:00")
        )
    ]

    # Add to session and commit
    with app.app_context():
        try:
            db.create_all()  # Ensure tables exist
            db.session.bulk_save_objects(users + databases)
            db.session.commit()
            print("Data seeded successfully!")
        except Exception as e:
            print(f"An error occurred while seeding data: {e}")


if __name__ == "__main__":
    seed_data()
