from flask_injector import inject
from flask import Response, jsonify
from src.dal.database import db
from src.models.db_model import Car, Brand, CarModel

class CompatRepository:
    
    def create_full_data(self, vehicle_name: str, brand_name: str, car_version: str, year: str, specifications: str):
        brand = Brand.query.filter_by(brand_name=brand_name).first()
        if not brand:
            brand = Brand(brand_name=brand_name)
            db.session.add(brand)
            db.session.flush()
        
        car = Car.query.filter_by(vehicle_name=vehicle_name).first()
        if not car:    
            car = Car(
                vehicle_name=vehicle_name,
                id_brand=brand.id_brand)
            db.session.add(car)
            db.session.flush()
        
        car_model = CarModel.query.filter_by(car_version=car_version).first()    
        if not car_model:
            car_model = CarModel(
                id_car=car.id_car,
                car_version=car_version,
                year=year,
                specifications=specifications)
            db.session.add(car_model)
        
        try:
            db.session.commit()
            return jsonify({'success': "Data created successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f"Error creating full data: {str(e)}"}), 500
        finally:
            db.session.close()
            
    def get_all_cars(self):
        return Car.query.all()
        
    def get_all_brands(self):
        brands = Brand.query.all()
        if not brands:
            return jsonify({'message': 'No brands found'}), 404
        return brands
    
    def create_car_structure(self, brand_name: str, vehicle_name: str, car_version: str, year: str, specifications: str):
        try:
            brand = Brand.query.filter_by(brand_name=brand_name).first()
            if not brand:
                brand = Brand(brand_name=brand_name)
                db.session.add(brand)
                db.session.flush()

            car = Car.query.filter_by(vehicle_name=vehicle_name, id_brand=brand.id_brand).first()
            if not car:
                car = Car(vehicle_name=vehicle_name, id_brand=brand.id_brand)
                db.session.add(car)
                db.session.flush()

            model_exists = CarModel.query.filter_by(id_car=car.id_car, car_version=car_version, year=year).first()
            if not model_exists:
                model = CarModel(
                    id_car=car.id_car,
                    car_version=car_version,
                    year=year,
                    specifications=specifications
                )
                db.session.add(model)

            return vehicle_name, None

        except Exception as e:
            db.session.rollback()
            return vehicle_name, str(e)
    
    def get_models_by_brand(self, brand_id: int):
        brand = Brand.query.get(brand_id)
        if not brand:
            return None, []

        cars = Car.query.filter_by(id_brand=brand_id).all()
        return brand, cars
    
    def get_brand(self, brand_name: str):
        try:
            brand = Brand.query.filter_by(brand_name=brand_name).first()
            if not brand:
                return None
            return brand
        except Exception as e:
            return "error", str(e)
        finally:
            db.session.close()
            
    def get_car(self, vehicle_name: str):
        try:
            response =  Car.query.filter_by(vehicle_name=vehicle_name.lower()).first()
            return response
        except Exception as e:
            raise e
            
    def get_model_by_id_car(self, id_car: int):
        try:
            car = Car.query.get(id_car)
            if not car:
                return None
            models = CarModel.query.filter_by(id_car=id_car).all()
            if not models:
                return None
            return models
        except Exception as e:
            raise e
        finally:
            db.session.close()
    
    def get_car_by_brand(self, id_brand: int):
        try:
            cars = Car.query.filter_by(id_brand=id_brand).all()
            if not cars:
                return None
            return cars
        except Exception as e:
            raise e
        finally:
            db.session.close()
    
    def get_year_by_id_car(self, id_car: int):
        try:
            car = Car.query.get(id_car)
            if not car:
                return None

            models = CarModel.query.filter_by(id_car=id_car).all()
            if not models:
                return None

            return models
        except Exception as e:
            raise e
        finally:
            db.session.close()
            
    def get_model_car(self, car_version: str):
        try:
            model = CarModel.query.filter_by(
                car_version=car_version.lower()).all()
            return model
        except Exception as e:
            return "error", str(e)
        finally:
            db.session.close()
            
    def get_model_by_id(self, id_model: int):
        model = CarModel.query.get(id_model)
        return model
            
    def select_model(self, id_brand: int, id_car: int, year: str):
        try:
            brand = Brand.query.get(id_brand)
            car = Car.query.filter_by(id_brand=id_brand, id_car=id_car).first()
            model = CarModel.query.filter_by(id_car=id_car, year=year).first()

            if not all([brand, car, model]):
                return None

            return {
                'brand_name': brand.brand_name,
                'vehicle_name': car.vehicle_name,
                'car_version': model.car_version,
                'year': model.year,
                'specifications': model.specifications
            }
        except Exception as e:
            raise e
        finally:
            db.session.close()
            
    def delete_model(self, id_model: int) -> bool:
        model = CarModel.query.get(id_model)
        if not model:
            return False

        db.session.delete(model)
        db.session.commit()
        return True
    
    def update_model(self, id_model: int, car_version: str, specifications: str):
        model = CarModel.query.get(id_model)
        if not model:
            return None
        try:
            model.car_version = car_version
            model.specifications = specifications
            db.session.commit()
            return model
        except Exception as e:
            db.session.rollback()
            raise e
        finally:
            db.session.close()