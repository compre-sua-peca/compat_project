from flask import Flask
from injector import Binder

from src.dal.database import DataBase


def application_injector(binder: Binder, app: Flask) -> Binder:
    binder.bind(DataBase, DataBase(app))

    return binder
