from flask import Response, jsonify
from flask_injector import inject
from src.dal.repositories.compat_repository import CompatRepository
from src.dal.database import db
from src.models.db_model import Car, Brand, CarModel
import pandas as pd


class ProjectService:
    @inject
    def __init__(self, Repository: CompatRepository) -> None:
        self.repository = Repository
        pass

    def create_full_data(self, json_data: dict):
        vehicle_name = json_data['vehicle_name'].lower()
        brand_name = json_data['brand_name'].lower()
        car_version = json_data['car_version'].lower()
        year = json_data['year']
        specifications = json_data['specifications'].lower()

        if Car.query.filter_by(vehicle_name=vehicle_name).first():
            return jsonify({'error': 'vehicle already exists'}), 400

        create_register = self.repository.create_full_data(
            vehicle_name=vehicle_name,
            brand_name=brand_name,
            car_version=car_version,
            year=year,
            specifications=specifications
        )
        return create_register

    def get_all_cars(self):
        cars = self.repository.get_all_cars()

        if not cars:
            return jsonify({'message': 'No cars found'}), 400

        return jsonify([{
            'id_car': car.id_car,
            'vehicle_name': car.vehicle_name,
            'brand_name': car.brand.brand_name,
            'models': [{
                'id_model': model.id_model,
                'car_version': model.car_version,
                'year': model.year,
                'specifications': model.specifications
            } for model in car.models]
        } for car in cars]), 200

    def get_all_brand(self):
        brands = self.repository.get_all_brands()
        brands_list = [
            {
                "id_brand": brand.id_brand,
                "brand_name": brand.brand_name
            }
            for brand in brands
        ]
        return jsonify(brands_list), 200

    def create_cars_by_xlsx(self, file):
        success = []
        errors = []

        try:
            df = pd.read_excel(file)

            for i, row in df.iterrows():
                brand_name = str(row['brand_name']).lower()
                vehicle_name = str(row['vehicle_name']).lower()
                car_version = str(row['vehicle_name']).lower()
                year = str(row['year'])
                specifications = str(row['vehicle_name']).lower()

                vehicle, error = self.repository.create_car_structure(
                    brand_name=brand_name,
                    vehicle_name=vehicle_name,
                    car_version=car_version,
                    year=year,
                    specifications=specifications
                )

                if error:
                    errors.append({
                        'row': i + 2,
                        'vehicle_name': row.get('vehicle_name'),
                        'error': error
                    })
                else:
                    success.append(vehicle)

            db.session.commit()

            return jsonify({
                'success': f'{len(success)} cars processed',
                'errors': errors
            }), 207 if errors else 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()

    def get_model_by_brand(self, brand_id: int):
        brand, cars = self.repository.get_models_by_brand(brand_id)

        if not brand:
            return {"error": "Brand not found"}, 500
        if not cars:
            return {"error": "No vehicles found for this brand"}, 500

        response_data = {
            "brand": brand.brand_name,
            "vehicles": [
                {
                    "vehicle_name": car.vehicle_name,
                    "models": [
                        {
                            "car_version": model.car_version,
                            "car_id": model.id_model,
                            "specifications": model.specifications
                        }
                        for model in CarModel.query.filter_by(id_car=car.id_car).all()
                    ]
                }
                for car in cars
            ]
        }

        return response_data, 200 

    def get_brand(self, brand_name: str):
        if not brand_name:
            return jsonify({'error': 'Brand name is required'}), 400
        brand = self.repository.get_brand(brand_name)
        return jsonify({"brand_name": brand.brand_name,
                        "brand_id": brand.id_brand}), 200

    def get_car(self, vehicle_name: str):
        try:
            car = self.repository.get_car(vehicle_name)
            if not car:
                return jsonify({'error': 'Car not found'}), 500

            return jsonify({
                'id_car': car.id_car,
                'vehicle_name': car.vehicle_name,
                'brand_name': car.brand.brand_name
            }), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_model_by_id_car(self, id_car: int):
        try:
            models = self.repository.get_model_by_id_car(id_car)
            if not models:
                
                return jsonify({'error': 'No models found for this car'}), 500
            return jsonify([{
                'id_model': model.id_model,
                'car_version': model.car_version,
                'year': model.year,
                'specifications': model.specifications
            } for model in models]), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def get_car_by_brand(self, id_brand: int):
        try:
            cars = self.repository.get_car_by_brand(id_brand)
            if not cars:
                return jsonify({'error': 'No cars found for this brand'}), 500

            return jsonify([{
                'id_car': car.id_car,
                'vehicle_name': car.vehicle_name
            } for car in cars]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def get_year_by_id_car(self, id_car: int):
        try:
            models = self.repository.get_year_by_id_car(id_car)
            if not models:
                return jsonify({'error': 'No models found for this car'}), 500
            return jsonify([{
                'year': model.year
            } for model in models]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def get_model_car(self, car_version: str):
        try:
            models = self.repository.get_model_car(car_version)
            if not models:
                return jsonify({'error': 'Model not found'}), 500

            if not isinstance(models, list):
                models = [models]
            response = [
                {
                    'id_model': model.id_model,
                    'car_version': model.car_version,
                    'year': model.year,
                    'specifications': model.specifications
                }
                for model in models
            ]

            return jsonify(response), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            db.session.close()

    def get_model_by_id(self, model_id: int):
        try:
            model = self.repository.get_model_by_id(model_id)
            if not model:
                return jsonify({'error': 'Model not found'}), 404
            return jsonify({
                'id_model': model.id_model,
                'car_version': model.car_version,
                'year': model.year,
                'specifications': model.specifications}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def select_model(self, id_brand: int, id_car: int, year: str):
        try:
            response = self.repository.select_model(id_brand, id_car, year)
            if not response:
                return jsonify({'error': 'Model not found'}), 404
            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def delete_model(self, id_model: int):
        try:
            deleted = self.repository.delete_model(id_model)
            if not deleted:
                return jsonify({'error': 'Model not found'}), 404

            return jsonify({'message': 'Model deleted successfully'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
            

    def update_model(self, json_data: dict):
        model_id: int = json_data['model_id']
        car_version: str = json_data['car_version']
        specifications: str = json_data['specifications']

        try:
            model = self.repository.update_model(
                id_model=model_id,
                car_version=car_version,
                specifications=specifications
            )

            if not model:
                return jsonify({'error': 'Model not found'}), 404

            return jsonify({
                'message': 'Model updated successfully',
                "update": {
                    "id_model": model.id_model,
                    "car_version": model.car_version,
                    "year": model.year,
                    "specifications": model.specifications
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()