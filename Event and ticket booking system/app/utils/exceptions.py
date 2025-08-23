from fastapi import HTTPException, status

class UserAlreadyExistsException(Exception):
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    def __init__(self, message: str = "Invalid credentials"):
        self.message = message
        super().__init__(self.message)

class EventNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

class VenueNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Venue not found")

class BookingNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
