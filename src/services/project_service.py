
from flask import Response, jsonify
from flask_injector import inject
from src.dal.repositories.example_repository import ExampleRepository
from src.dal.database import db
from src.models.db_model import Car, Brand, CarModel
import pandas as pd


class ProjectService:
    @inject
    def __init__(self) -> None:
        pass

    def create_full_data(self, json_data: dict):
        if Car.query.filter_by(vehicle_name=json_data['vehicle_name'].lower()).first():
            return jsonify({'error': 'Veículo já existe'}), 400

        new_brand = Brand(
            brand_name=json_data['brand_name'].lower()
        )
        db.session.add(new_brand)
        db.session.flush()

        new_car = Car(
            vehicle_name=json_data['vehicle_name'].lower(),
            id_brand=new_brand.id_brand
        )
        db.session.add(new_car)
        db.session.flush()

        new_model = CarModel(
            id_car=new_car.id_car,
            car_version=json_data['car_version'].lower(),
            year=json_data['year'],
            specifications=json_data['specifications'].lower()
        )
        try:
            db.session.add(new_model)
            db.session.commit()
            return jsonify({'success': "Data created successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def get_all_cars(self):
        cars = Car.query.all()
        if not cars:
            return jsonify({'message': 'No cars found'}), 404
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

    def create_cars_by_xlsx(self, file):
        success = []
        errors = []

        try:
            df = pd.read_excel(file)

            for i, row in df.iterrows():
                try:
                    brand_name = str(row['brand_name']).lower()
                    vehicle_name = str(row['vehicle_name']).lower()
                    car_version = str(row['vehicle_name']).lower()
                    year = str(row['year'])
                    specifications = str(row['vehicle_name']).lower()

                    # Verifica se a marca já existe
                    brand = Brand.query.filter_by(
                        brand_name=brand_name).first()

                    if not brand:
                        # Cria nova marca
                        brand = Brand(brand_name=brand_name)
                        db.session.add(brand)
                        db.session.flush()  # garante que o ID da marca seja gerado

                    # Verifica se o carro já existe
                    car = Car.query.filter_by(
                        vehicle_name=vehicle_name, id_brand=brand.id_brand).first()
                    if not car:
                        car = Car(vehicle_name=vehicle_name,
                                  id_brand=brand.id_brand)
                        db.session.add(car)
                        db.session.flush()

                    # Verifica se o modelo já existe
                    model_exists = CarModel.query.filter_by(
                        id_car=car.id_car,
                        car_version=car_version,
                        year=year
                    ).first()

                    if not model_exists:
                        model = CarModel(
                            id_car=car.id_car,
                            car_version=car_version,
                            year=year,
                            specifications=specifications
                        )
                        db.session.add(model)

                    success.append(vehicle_name)

                except Exception as e:
                    db.session.rollback()
                    errors.append({
                        'row': i + 2,
                        'vehicle_name': row.get('vehicle_name'),
                        'error': str(e)
                    })

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
        if not brand_id:
            return jsonify({'error': 'Brand ID is required'}), 400

        brand = Brand.query.get(brand_id)
        if not brand:
            return jsonify({'error': 'Brand not found'}), 404

        cars = Car.query.filter_by(id_brand=brand_id).all()
        if not cars:
            return jsonify({'error': 'No vehicles found for this brand'}), 404

        response_data = {
            "brand": brand.brand_name,
            "vehicles": []
        }

        for car in cars:
            models = CarModel.query.filter_by(id_car=car.id_car).all()

            response_data["vehicles"].append({
                "vehicle_name": car.vehicle_name,
                "models": [{
                    "car_version": model.car_version,
                    "year": model.year,
                    "specifications": model.specifications
                } for model in models]
            })
        return jsonify(response_data), 200

    def get_brand(self, brand_name: str):
        try:
            brand = Brand.query.filter_by(
                brand_name=brand_name.lower()).first()
            if not brand:
                return jsonify({'error': 'Brand not found'}), 404

            return jsonify({
                'id_brand': brand.id_brand,
                'brand_name': brand.brand_name}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def get_car(self, vehicle_name: str):
        try:
            car = Car.query.filter_by(
                vehicle_name=vehicle_name.lower()).first()
            if not car:
                return jsonify({'error': 'Car not found'}), 404

            return jsonify({
                'id_car': car.id_car,
                'vehicle_name': car.vehicle_name,
                'brand_name': car.brand.brand_name}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def get_model_car(self, car_version: str):
        try:
            model = CarModel.query.filter_by(
                car_version=car_version.lower()).first()
            if not model:
                return jsonify({'error': 'Car model not found'}), 404

            return jsonify({
                'id_model': model.id_model,
                'car_version': model.car_version,
                'year': model.year,
                'specifications': model.specifications}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def delete_model(self, model_id: int):
        try:
            model = CarModel.query.get(model_id)
            if not model:
                return jsonify({'error': 'Model not found'}), 404

            db.session.delete(model)
            db.session.commit()
            return jsonify({'message': 'Model deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            db.session.close()

    def update_model(self, json_data: dict):
        model_id: int = json_data['model_id']
        car_version: str = json_data['car_version']
        specifications: str = json_data['specifications']
        try:
            model = CarModel.query.get(model_id)
            if not model:
                return jsonify({'error': 'Model not found'}), 404

            model.car_version = car_version
            model.specifications = specifications

            db.session.add(model)
            db.session.commit()
            db.session.refresh(model)
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