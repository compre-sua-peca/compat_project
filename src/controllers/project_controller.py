from flask import jsonify
from flask_injector import inject
from src.services.project_service import ProjectService

class ProjectController:
    @inject
    def __init__(self, Service: ProjectService) -> None:
        self.service = Service

    def create_car(self, request):
        json_data = request.get_json()
        response = self.service.create_full_data(json_data)
        return response

    def create_car_from_excel(self, request):
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file provided'}), 400
        try:
            response = self.service.create_cars_by_xlsx(file)
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_all_cars(self):
        response = self.service.get_all_cars()
        return response

    def get_models_by_brand(self, id_brand: int):
        if not id_brand:
            return jsonify({'error': 'Brand name is required'}), 400

        try:
            models = self.service.get_model_by_brand(id_brand)
            return models
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_brand(self, brand_name: str):
        if not brand_name:
            return jsonify({'error': 'Brand name is required'}), 400

        brand = self.service.get_brand(brand_name)
        return brand

    def get_car(self, vehicle_name: str):
        if not vehicle_name:
            return jsonify({'error': 'Vehicle name is required'}), 400

        car = self.service.get_car(vehicle_name)
        return car
    
    def get_car_by_brand(self, id_brand: int):
        if not id_brand:
            return jsonify({'error': 'Brand ID is required'}), 400

        try:
            cars = self.service.get_car_by_brand(id_brand)
            return cars
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def get_model_by_id_car(self, id_car: int):
        if not id_car:
            return jsonify({'error': 'Car ID is required'}), 400

        try:
            models = self.service.get_model_by_id_car(id_car)
            return models
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    def get_year_by_id_car(self, id_car: int):
        if not id_car:
            return jsonify({'error': 'Car ID is required'}), 400

        try:
            years = self.service.get_year_by_id_car(id_car)
            return years
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_all_brands(self):
        return self.service.get_all_brand()
    
    def get_model_car(self, car_version: str):
        if not car_version:
            return jsonify({'error': 'Car version is required'}), 400

        model = self.service.get_model_car(car_version)
        return model
    
    def get_model_by_id(self, id_model: int):
        if not id_model:
            return jsonify({'error': 'Model ID is required'}), 400

        try:
            model = self.service.get_model_by_id(id_model)
            return model
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def select_model(self, id_brand: int, id_car: int, year: str):
        if not id_brand or not id_car or not year:
            return jsonify({'error': 'Brand ID, Car ID, and Year are required'}), 400

        try:
            model = self.service.select_model(id_brand, id_car, year)
            return model
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    def delete_model(self, id_model: int):
        if not id_model:
            return jsonify({'error': 'Model ID is required'}), 400

        try:
            self.service.delete_model(id_model)
            return jsonify({'message': 'Model deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        
    def update_model(self, request):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'Invalid data provided'}), 400

        try:
            response = self.service.update_model(json_data)
            return response
        except Exception as e:
            return jsonify({'error': str(e)}), 500