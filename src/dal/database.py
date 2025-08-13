from typing import Optional
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

class DataBase:
    def __init__(self, app: Flask) -> None:
        self.app = app

        self.configure_app()
        self.configure_db()
        self.configure_migrations()

    def configure_app(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_ECHO'] = os.getenv("SQLALCHEMY_ECHO", False) #Se true, retorna as queries SQL no console

    def configure_db(self):
        db.init_app(self.app)

    def configure_migrations(self):
        migrate.init_app(self.app, db)