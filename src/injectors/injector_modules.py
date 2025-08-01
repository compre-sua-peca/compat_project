from flask import Flask
from injector import Binder

from src.injectors.application_injector import application_injector
from src.injectors.project_injector import project_injector


def injector_modules(binder: Binder, app: Flask) -> Binder:
    binder = application_injector(binder, app)
    binder = project_injector(binder)
    return binder
