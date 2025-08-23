import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

class Config:
#Database
    MONGO_URI: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME: str = os.getenv("DB_NAME", "event_ticket_booking")

#JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", 30))

#Email (SMTP)
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    EMAIL_USER: str = os.getenv("EMAIL_USER", "your_email@example.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "your_password")

#Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
