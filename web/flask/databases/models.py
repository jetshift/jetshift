from datetime import datetime
from web.flask.main import app, db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


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
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Database {self.name}>'

# Create tables
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
