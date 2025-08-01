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
        self.app.config['SQLALCHEMY_ECHO'] = os.getenv("SQLALCHEMY_ECHO", False)

    def configure_db(self):
        db.init_app(self.app)

    def configure_migrations(self):
        migrate.init_app(self.app, db)

    # def setup_async_sqlalchemy(self):
    #     db_url = self.app.config["SQLALCHEMY_DATABASE_URI"]

    #     # Cria engine assíncrono
    #     self.async_engine = create_async_engine(
    #         db_url,
    #         echo=self.app.config.get("SQLALCHEMY_ECHO", False),
    #         future=True,
    #     )

    #     # Cria sessionmaker assíncrono
    #     self.async_session_factory = sessionmaker(
    #         self.async_engine,
    #         expire_on_commit=False,
    #         class_=AsyncSession,
    #     )

    #     # Atribui ao db global para reuso em outras partes do app
    #     db.async_session = self.async_session_factory