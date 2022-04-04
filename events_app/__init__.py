from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from events_app.config import Config
import os
# from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from events_app.routes import main

app.register_blueprint(main)

db.init_app(app)

with app.app_context():
    db.create_all()  # Create sql tables for our data models
