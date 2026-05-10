"""
Error classes for the Lindo SDK.

Provides custom exception classes for common HTTP error codes and API errors.
These errors include status codes and descriptive messages for debugging.

@satisfies Requirements 6.4
"""

from typing import Optional, Dict, List


class LindoError(Exception):
    """
    Base exception class for all Lindo SDK errors.
    Contains the HTTP status code and error message.
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        code: str = "LINDO_ERROR",
    ) -> None:
        """
        Initialize a LindoError.

        Args:
            message: Human-readable error message
            status_code: HTTP status code of the error response
            code: Error code for programmatic handling
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code

    def __str__(self) -> str:
        return f"{self.code}: {self.message} (status: {self.status_code})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code}, code={self.code!r})"


class AuthenticationError(LindoError):
    """
    Exception raised when authentication fails (HTTP 401).
    This typically occurs when the API key is invalid or expired.
    """

    def __init__(
        self,
        message: str = "Authentication failed. Please check your API key.",
    ) -> None:
        super().__init__(message, 401, "AUTHENTICATION_ERROR")


class ForbiddenError(LindoError):
    """
    Exception raised when the request is forbidden (HTTP 403).
    This typically occurs when the user doesn't have permission to access the resource.
    """

    def __init__(
        self,
        message: str = "Access forbidden. You do not have permission to access this resource.",
    ) -> None:
        super().__init__(message, 403, "FORBIDDEN_ERROR")


class NotFoundError(LindoError):
    """
    Exception raised when a resource is not found (HTTP 404).
    This typically occurs when the requested resource doesn't exist.
    """

    def __init__(
        self,
        message: str = "Resource not found.",
    ) -> None:
        super().__init__(message, 404, "NOT_FOUND_ERROR")


class ValidationError(LindoError):
    """
    Exception raised when the request is invalid (HTTP 400).
    This typically occurs when the request body or parameters are malformed.
    """

    def __init__(
        self,
        message: str = "Validation failed.",
        errors: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """
        Initialize a ValidationError.

        Args:
            message: Human-readable error message
            errors: Optional dictionary of field-specific validation errors
        """
        super().__init__(message, 400, "VALIDATION_ERROR")
        self.errors = errors


class RateLimitError(LindoError):
    """
    Exception raised when rate limit is exceeded (HTTP 429).
    This typically occurs when too many requests are made in a short period.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please try again later.",
        retry_after: Optional[int] = None,
    ) -> None:
        """
        Initialize a RateLimitError.

        Args:
            message: Human-readable error message
            retry_after: Time in seconds until the rate limit resets
        """
        super().__init__(message, 429, "RATE_LIMIT_ERROR")
        self.retry_after = retry_after


class ServerError(LindoError):
    """
    Exception raised when the server encounters an internal error (HTTP 500).
    This typically indicates a problem on the server side.
    """

    def __init__(
        self,
        message: str = "Internal server error. Please try again later.",
    ) -> None:
        super().__init__(message, 500, "SERVER_ERROR")


class NetworkError(LindoError):
    """
    Exception raised when a network error occurs.
    This typically occurs when the request cannot be completed due to network issues.
    """

    def __init__(
        self,
        message: str = "Network error. Please check your connection.",
    ) -> None:
        super().__init__(message, 0, "NETWORK_ERROR")


class TimeoutError(LindoError):
    """
    Exception raised when a request times out.
    This typically occurs when the server takes too long to respond.
    """

    def __init__(
        self,
        message: str = "Request timed out. Please try again.",
    ) -> None:
        super().__init__(message, 0, "TIMEOUT_ERROR")


def create_error_from_status(
    status_code: int,
    message: str,
    retry_after: Optional[int] = None,
) -> LindoError:
    """
    Maps an HTTP status code to the appropriate error class.

    Args:
        status_code: The HTTP status code
        message: The error message
        retry_after: Optional retry-after value for rate limit errors

    Returns:
        The appropriate error instance
    """
    if status_code == 400:
        return ValidationError(message)
    elif status_code == 401:
        return AuthenticationError(message)
    elif status_code == 403:
        return ForbiddenError(message)
    elif status_code == 404:
        return NotFoundError(message)
    elif status_code == 429:
        return RateLimitError(message, retry_after)
    elif status_code in (500, 502, 503, 504):
        return ServerError(message)
    else:
        return LindoError(message, status_code)
