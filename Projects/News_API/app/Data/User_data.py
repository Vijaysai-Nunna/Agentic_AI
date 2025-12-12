from app.Utils.decorators import handle_exceptions
from app.Utils.logger import get_logger
import os,json

logging = get_logger(__name__)

@handle_exceptions
def save_to_json(data, filename):
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logging.info(f"Saved output to {filename}")