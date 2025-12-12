from functools import wraps
from fastapi import HTTPException
from app.utils.logger import get_logger

logger = get_logger(__name__)

#creating an function for exception handling
def handle_exception(func):
    # The decorators that wraps the original function

    @wraps(func) # this decorator preserves the orginial function's name and docstring

    def wrapper(*args,**kwargs):

        try:
            logger.info(f"Excuting : {func.__name__}")
            return func(*args,**kwargs)

        except Exception as e:
            logger.exception(f"Error while Excuting  {func.__name__}  : {e} ")
            raise HTTPException(
                status_code = 400,
                detail = str(e)

            )

        return wrapper