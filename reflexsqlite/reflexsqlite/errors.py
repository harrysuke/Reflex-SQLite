"""Typed application errors.

Handlers convert these into friendly, user-facing messages; nothing here leaks
stack traces or raw database errors to the browser.
"""
from __future__ import annotations


class AppError(Exception):
    code = "APP_ERROR"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(AppError):
    code = "VALIDATION_ERROR"


class NotFoundError(AppError):
    code = "NOT_FOUND"


class DuplicateError(AppError):
    code = "DUPLICATE"


class AuthenticationError(AppError):
    code = "AUTHENTICATION_ERROR"


class AuthorizationError(AppError):
    code = "AUTHORIZATION_ERROR"


class LibraryUnavailableError(AppError):
    code = "LIBRARY_UNAVAILABLE"


class UploadError(AppError):
    code = "UPLOAD_ERROR"


USER_MESSAGES = {
    "VALIDATION_ERROR": "Please check the values you entered.",
    "NOT_FOUND": "That item no longer exists.",
    "DUPLICATE": "An item with those details already exists.",
    "AUTHENTICATION_ERROR": "Your session has expired. Please sign in again.",
    "AUTHORIZATION_ERROR": "You do not have permission to do that.",
    "LIBRARY_UNAVAILABLE": "This library is not installed in the current environment.",
    "UPLOAD_ERROR": "The dataset could not be read.",
    "APP_ERROR": "Something went wrong. Please try again.",
}


def friendly(error: Exception) -> str:
    """Map any exception to a safe, human-readable message."""
    if isinstance(error, AppError):
        # Known, operational errors are safe to show verbatim.
        return error.message
    return USER_MESSAGES["APP_ERROR"]
