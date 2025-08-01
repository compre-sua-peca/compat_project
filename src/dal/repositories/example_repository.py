from flask_injector import inject

from src.dal.database import DataBase
from src.exceptions.example_exceptions import UnexpectedException

class ExampleRepository:
    @inject
    def __init__(self, database: DataBase) -> None:
        self.database: DataBase = database

    def example_repository_operation(self, example_data: str):
        item = self.database.example_database_operation('ExampleTableName', example_data, 'exampleKeyName')

        if item is None:
            return None

        required_fields = ['example_attribute']
        example_data = {}

        for field in required_fields:
            value = item.get(field)
            if value is None:
                raise UnexpectedException
            example_data[field] = value

        example = "ExampleData"
        return example