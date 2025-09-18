from fastapi import HTTPException, status

class UserAlreadyExistsException(Exception):
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Token is invalid or user logged out"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class EventNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

class VenueNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")

class BookingNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

class PasswordMismatchException(Exception):
    """Raised when password and confirm password do not match during registration or update."""
    pass

class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Unauthorized: Only admins can access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )
# --------------------Admin-specific exceptions-------------------
class AdminAlreadyExistsException(Exception):
    pass

class AdminNotFoundException(Exception):
    pass

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

# -------------Event-specific exception----------------
class EventAlreadyExistsException(Exception):
    def __init__(self, message: str = "Event already exists"):
        self.message = message
        super().__init__(self.message)

# ---------- Venue Exceptions ----------
class VenueAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "Venue with the same name already exists"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
class VenueNotFoundException(HTTPException):
    def __init__(self, message: str = "Venue not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class VenueAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "Venue already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)