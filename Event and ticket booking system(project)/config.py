import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT Config
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# MongoDB Config
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "Event_Ticket_db")

# Other Configs (optional)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")