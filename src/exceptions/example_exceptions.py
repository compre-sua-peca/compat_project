from src.utils.format_message import format_message


class ExampleException(Exception):

    def __init__(self, http_code: int, logger_message: str, response_message: str) -> None:
        self.http_code = http_code
        self.logger_message = format_message(logger_message)
        self.response_message = format_message(response_message)


class UnexpectedException(ExampleException):

    def __init__(self, http_code=500, logger_message='erro inesperado no servidor', response_message='erro interno do servidor') -> None:
        super().__init__(http_code, logger_message, response_message)