from fastapi import status


class CustomException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


class BadRequestException(CustomException):
    def __init__(self, message: str, status_code: int = 400):
        super(BadRequestException, self).__init__(message=message, status_code=status_code)


class UnauthorizedException(CustomException):
    def __init__(self, message: str):
        super(UnauthorizedException, self).__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(CustomException):
    def __init__(self, message: str):
        super(ForbiddenException, self).__init__(message, status.HTTP_403_FORBIDDEN)


class NotFoundException(CustomException):
    def __init__(self, message: str):
        super(NotFoundException, self).__init__(message, status.HTTP_404_NOT_FOUND)


class MethodNotAllowedException(CustomException):
    def __init__(self, message: str):
        super(MethodNotAllowedException, self).__init__(message, status.HTTP_405_METHOD_NOT_ALLOWED)


class FailedDependency(CustomException):
    def __init__(self, message: str):
        super(FailedDependency, self).__init__(message, status.HTTP_424_FAILED_DEPENDENCY)
