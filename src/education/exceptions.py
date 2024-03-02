from http import HTTPStatus

from config.base_error import BaseError


class NoAvailibleGroupsException(BaseError):
    detail = "All groups are filled and lessons started"
    status_code = HTTPStatus.BAD_REQUEST


class UserAlreadyAddedToProductException(BaseError):
    detail = "User already added to product"
    status_code = HTTPStatus.BAD_REQUEST