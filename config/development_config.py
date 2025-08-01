from config.config import Config
import os

class DevelopmentConfig(Config):
    PORT = 5000
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "0.0.0.0"
