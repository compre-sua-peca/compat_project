import sys
import os

from config.development_config import DevelopmentConfig
from flask import Flask
from flask_cors import CORS
from flask_dotenv import DotEnv
from flask_injector import FlaskInjector
from src.injectors.injector_modules import injector_modules
from src.routes import register_blueprints


app = Flask(__name__)

CORS(app)

if not os.path.exists('.env'):
    with open('.env', 'w') as file_env:
        file_env.write('')

dotenv = DotEnv()
dotenv.init_app(app)

app.config.from_object(DevelopmentConfig)

register_blueprints(app)

FlaskInjector(app, modules=[lambda binder: injector_modules(binder, app)])

if __name__ == '__main__':
    print('Starting application.')
    try:
        app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))    
    except Exception as e:
        sys.exit(1)
    print('Closing application.')
