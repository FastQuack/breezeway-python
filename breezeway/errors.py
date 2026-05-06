from datetime import datetime


class APIClientError(Exception):
    """
    Base class for all Breezeway client errors.
    """
    pass

class AuthenticationError(APIClientError):
    """
    Error raised when authentication fails.
    """
    pass

class InvalidAttachmentError(APIClientError):
    """
    Error raised when an invalid attachment is provided.
    """
    pass

class MultipleCompaniesError(APIClientError):
    """
    Error raised when company_id is not provided,
    and there are multiple companies associated with the client.
    """
    pass

class NoCompaniesError(APIClientError):
    pass

class NotFoundError(APIClientError): pass

class RateLimitExceeded(APIClientError):
    def __init__(self, response: dict | None = None):
        if not response or 'details' not in response or 'message' not in response['details'] or 'retry_after' not in response['details']:
            raise ValueError("Invalid response format for RateLimitExceeded")
        super().__init__(response['details']['message'])
        self.retry_after: datetime = datetime.fromisoformat(response['details']['retry_after'])

    @property
    def is_expired(self) -> bool:
        """Check if the rate limit is expired."""
        return datetime.now() > self.retry_after

class UnauthorizedError(APIClientError): pass
