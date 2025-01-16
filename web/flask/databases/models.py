from datetime import datetime, timezone
from web.flask.main import app, db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'


class Database(db.Model):
    __tablename__ = 'databases'

    id = db.Column(db.Integer, primary_key=True)
    dialect = db.Column(db.String(50), nullable=False)  # e.g., mysql, postgres
    type = db.Column(db.String(50), nullable=False)  # e.g., source, target
    title = db.Column(db.String(120), nullable=False)
    host = db.Column(db.String(191), nullable=True)
    port = db.Column(db.Integer, nullable=True)
    username = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(191), nullable=True)
    database = db.Column(db.String(191), nullable=True)
    status = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Backref for MigrateDatabase
    source_migrations = db.relationship(
        'MigrateDatabase', foreign_keys='MigrateDatabase.source_db_id', back_populates='source_db'
    )
    target_migrations = db.relationship(
        'MigrateDatabase', foreign_keys='MigrateDatabase.target_db_id', back_populates='target_db'
    )

    # Backref for MigrateTable
    source_table_jobs = db.relationship(
        'MigrateTable', foreign_keys='MigrateTable.source_db_id', back_populates='source_db'
    )
    target_table_jobs = db.relationship(
        'MigrateTable', foreign_keys='MigrateTable.target_db_id', back_populates='target_db'
    )

    def __repr__(self):
        return f'<Database {self.id}>'


class MigrateDatabase(db.Model):
    __tablename__ = 'migrate_databases'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    source_db_id = db.Column(db.Integer, db.ForeignKey('databases.id'), nullable=False)
    target_db_id = db.Column(db.Integer, db.ForeignKey('databases.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    logs = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    source_db = db.relationship('Database', foreign_keys=[source_db_id], back_populates='source_migrations')
    target_db = db.relationship('Database', foreign_keys=[target_db_id], back_populates='target_migrations')

    def __repr__(self):
        return f'<MigrateDatabase {self.id}>'


class MigrateTable(db.Model):
    __tablename__ = 'migrate_tables'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    source_db_id = db.Column(db.Integer, db.ForeignKey('databases.id'), nullable=False)
    target_db_id = db.Column(db.Integer, db.ForeignKey('databases.id'), nullable=False)
    source_tables = db.Column(db.Text, nullable=True)
    target_tables = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=0)
    logs = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    source_db = db.relationship('Database', foreign_keys=[source_db_id], back_populates='source_table_jobs')
    target_db = db.relationship('Database', foreign_keys=[target_db_id], back_populates='target_table_jobs')

    def __repr__(self):
        return f'<MigrateDatabase {self.id}>'


# Create tables
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
