# --------------------------------------------
# ** SEMPRE adicionar sua blueprint nova aqui
# ** na lista "blueprints" para registrá-la
# ** na aplicação.
# --------------------------------------------

from flask import Flask

from src.routes.project_routes import project_bp

blueprints = [
    project_bp
]

def register_blueprints(app: Flask) -> None:
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
