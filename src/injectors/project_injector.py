from injector import Binder
from src.controllers.project_controller import ProjectController
from src.dal.database import DataBase
from src.services.project_service import ProjectService


def project_injector(binder: Binder) -> Binder:
    binder.bind(ProjectController, ProjectController)
    binder.bind(ProjectService, ProjectService)
    
    return binder
