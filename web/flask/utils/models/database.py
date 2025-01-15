from web.flask.databases.models import Database


def supported_dialects():
    return ["sqlite", "mysql", "postgresql"]


def get_database_list(db_type):
    databases = Database.query.filter_by(type=db_type)

    data = [
        {
            "id": db_entry.id,
            "dialect": db_entry.dialect,
            "type": db_entry.type,
            "name": db_entry.name,
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
                    message = f"Database '{database['name']}' connection successful. The first table in the database is: {first_table[0]}"
                else:
                    success = False
                    message = f"Database '{database['name']}' connection failed: " + database['database']
            else:
                connection.execute(text("SELECT 1"))
                connection.close()
                success = True
                message = f"Database '{database['name']}' connection successful."
    except OperationalError as e:
        original_error = str(e.orig)
        success = False
        message = f"Database '{database['name']}' connection failed: {original_error}"
    except Exception as e:
        success = False
        message = f"Database '{database['name']}' connection failed: {e}"

    return success, message
