from flask_sqlalchemy import SQLAlchemy

from web.flask.main import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///js.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
