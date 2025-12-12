import json
import os
from app.utils.logger import get_logger
from app.utils.decoraters import handle_exceptions

logger = get_logger(__name__)

@handle_exceptions
def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error while reading {file_path}: {str(e)}")
        return []

@handle_exceptions
def save_json(file_path, data):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving file {file_path}: {str(e)}")
        print(f"Error saving data to {file_path}: {e}")
