from web.flask.databases.models import Database


def supported_dialects():
    return ["sqlite", "mysql", "postgresql"]


def create_database(request):
    from web.flask.main import db

    try:
        data = request.get_json()

        print(data)

        # Check if a database with the same dialect, type, and title already exists
        existing_database = Database.query.filter_by(
            dialect=data.get("dialect"),
            type=data.get("type"),
            title=data.get("title")
        ).first()

        if existing_database:
            success = False
            message = "Database already exists"
            return success, message

        # Create a new Database instance
        new_database = Database(
            dialect=data.get("dialect"),
            type=data.get("type"),
            title=data.get("title"),
            host=data.get("host"),
            port=data.get("port"),
            username=data.get("username"),
            password=data.get("password"),
            database=data.get("database")
        )

        # Add to the database session and commit
        db.session.add(new_database)
        db.session.commit()

        success = True
        message = "Database added successfully"
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()

        success = False
        message = str(e)

    return success, message


def delete_database(database_id):
    from web.flask.main import db

    try:
        # Find the record by id
        database_entry = Database.query.get(database_id)
        if not database_entry:
            success = False
            message = "Database entry not found"
            return success, message

        # Delete the record
        db.session.delete(database_entry)
        db.session.commit()

        success = True
        message = "Database entry deleted successfully"
    except Exception as e:
        # Rollback in case of an error
        db.session.rollback()

        success = False
        message = str(e)

    return success, message


def check_database_connection(database):
    import os
    from sqlalchemy import text, create_engine
    from sqlalchemy.exc import OperationalError

    try:
        # Check supported dialects
        if database['dialect'] not in supported_dialects():
            raise ValueError(f"Unsupported dialect: {database['dialect']}")

        # Create database URL based on dialect
        if database['dialect'] == 'sqlite':
            path = "instance/" + database['database']

            # Check if the file exists
            if not os.path.isfile(path):
                raise ValueError(f"Database file does not exist: {database['database']}")

            database_url = "sqlite:///" + path
        if database['dialect'] == 'mysql':
            database_url = (
                f"mysql+pymysql://{database['username']}:{database['password']}@{database['host']}:{database['port']}/{database['database']}"
                "?connect_timeout=10"
            )
        if database['dialect'] == 'postgresql':
            database_url = (
                f"postgresql+psycopg://{database['username']}:{database['password']}@{database['host']}:{database['port']}/{database['database']}"
                "?connect_timeout=10"
            )

        engine = create_engine(database_url)
        with engine.connect() as connection:

            if database['dialect'] == 'sqlite':
                # Query sqlite_master for the first table
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                first_table = result.fetchone()
                print(first_table)
                if first_table:
                    success = True
                    message = f"Database '{database['title']}' connection successful. The first table in the database is: {first_table[0]}"
                else:
                    success = False
                    message = f"Database '{database['title']}' connection failed: " + database['database']
            else:
                connection.execute(text("SELECT 1"))
                connection.close()
                success = True
                message = f"Database '{database['title']}' connection successful."
    except OperationalError as e:
        original_error = str(e.orig)
        success = False
        message = f"Database '{database['title']}' connection failed: {original_error}"
    except Exception as e:
        success = False
        message = f"Database '{database['title']}' connection failed: {e}"

    return success, message


def get_database_list(db_type):
    databases = Database.query.filter_by(type=db_type).order_by(Database.id.desc())

    data = [
        {
            "id": db_entry.id,
            "title": db_entry.title,
            "dialect": db_entry.dialect,
            "type": db_entry.type,
            "host": db_entry.host,
            "port": db_entry.port,
            "username": db_entry.username,
            "database": db_entry.database,
            "status": db_entry.status,
            "created_at": db_entry.created_at.isoformat(),
            "updated_at": db_entry.updated_at.isoformat(),
        }
        for db_entry in databases
    ]

    return data
