from flask import Blueprint, Response, request, jsonify
from flask_injector import inject
from src.controllers.project_controller import ProjectController

project_bp = Blueprint('project', __name__)

@project_bp.route('/<int:id_model>', methods=['DELETE'])
@inject
def delete_model(project_controller: ProjectController, id_model: int) -> Response:
    return project_controller.delete_model(id_model)

@project_bp.route('/update-model', methods=['PUT'])
@inject
def update_model(project_controller: ProjectController) -> Response:
    return project_controller.update_model(request)

@project_bp.route('/create-car', methods=['POST'])
@inject
def creat_compat_full_data(project_controller: ProjectController) -> Response:
    return project_controller.create_car(request)

@project_bp.route('/create-from-excel', methods=['POST'])
@inject
def create_from_excel(project_controller: ProjectController) -> Response:
    return project_controller.create_car_from_excel(request)

@project_bp.route('/get-all-cars', methods=['GET'])
@inject
def get_all_cars(project_controller: ProjectController) -> Response:
    return project_controller.get_all_cars()

@project_bp.route('/models-brand/<int:id_brand>', methods=['GET'])
@inject
def get_models_by_brand(project_controller: ProjectController, id_brand: int) -> Response:
    return project_controller.get_models_by_brand(id_brand)

@project_bp.route('/select/<int:id_brand>/<int:id_car>/<string:year>', methods=['GET'])
@inject
def get_model_by_year(project_controller: ProjectController, id_brand: int, id_car: int, year: str) -> Response:
    return project_controller.select_model(id_brand, id_car, year)

@project_bp.route('/brand/<string:brand_name>', methods=['GET'])
@inject
def get_brand(project_controller: ProjectController, brand_name: str) -> Response:
    return project_controller.get_brand(brand_name)

@project_bp.route('/car/<string:vehicle_name>', methods=['GET'])
@inject
def get_car(project_controller: ProjectController, vehicle_name: str) -> Response:
    return project_controller.get_car(vehicle_name)

@project_bp.route('/model/<string:car_version>', methods=['GET'])
@inject
def get_model_car(project_controller: ProjectController, car_version: str) -> Response:
    return project_controller.get_model_car(car_version)

@project_bp.route('/year-models/<int:id_car>', methods=['GET'])
@inject
def get_year_models(project_controller: ProjectController, id_car: int) -> Response:
    return project_controller.get_year_by_id_car(id_car)

@project_bp.route('/car-by-brand/<int:id_brand>', methods=['GET'])
@inject
def get_car_by_brand(project_controller: ProjectController, id_brand: int) -> Response:
    return project_controller.get_car_by_brand(id_brand)

@project_bp.route('/models-id/<int:id_model>', methods=['GET'])
@inject
def get_model_by_id(project_controller: ProjectController, id_model: str) -> Response:
    return project_controller.get_model_by_id(id_model)

@project_bp.route('/model-by-idcar/<int:id_car>', methods=['GET'])
@inject
def get_model_by_id_car(project_controller: ProjectController, id_car:int) -> Response:
    return project_controller.get_model_by_id_car(id_car)

@project_bp.route('/all-brands', methods=['GET'])
@inject
def get_all_brands(project_controller: ProjectController) -> Response:
    return project_controller.get_all_brands()