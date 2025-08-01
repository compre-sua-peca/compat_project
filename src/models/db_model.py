from src.dal.database import db
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from src.dal.database import db
from sqlalchemy.orm import relationship


class Brand(db.Model):
    __tablename__ = 'brand'

    id_brand = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    brand_name = Column(String(100), unique=True, nullable=False)

    # Relationship: one brand has many cars
    cars = relationship('Car', back_populates='brand')

class Car(db.Model):
    __tablename__ = 'car'

    id_car = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    vehicle_name = Column(String(100), nullable=False)
    id_brand = Column(Integer, ForeignKey('brand.id_brand', ondelete='RESTRICT', onupdate='NO ACTION'), nullable=False)

    # Unique constraint on vehicle_name per design
    __table_args__ = (
        UniqueConstraint('vehicle_name', 'id_brand', name='ux_car_vehicle_brand'),
    )

    # Relationships
    brand = relationship('Brand', back_populates='cars')
    models = relationship('CarModel', back_populates='car', cascade='all, delete-orphan')

class CarModel(db.Model):
    __tablename__ = 'car_model'

    id_model = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_car = Column(Integer, ForeignKey('car.id_car', ondelete='NO ACTION', onupdate='NO ACTION'), nullable=False)
    car_version = Column(String(50), nullable=False)
    year = Column(String(10), nullable=False)
    specifications = Column(Text, nullable=False)

    __table_args__ = (
        # Garante que a combinação (id_car, year, car_version) seja única,
        # permitindo o mesmo veículo em anos diferentes, versões diferentes em mesmo ano,
        # mas impede duplicação exata de versão-ano para um mesmo veículo.
        UniqueConstraint('id_car', 'year', 'car_version', name='ux_car_model_unique'),
    )

    # Relationships
    car = relationship('Car', back_populates='models')
